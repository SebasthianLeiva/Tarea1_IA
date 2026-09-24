
import heapq

from metodos.general.agente import *
from metodos.general.distancia_manhattan import distancia_manhattan
import random


class Agente_a_estrella:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        # lista de casillas frontera, guarda como elementos tuplas, para que puedan
        #comparadas por heapq.heappush() y distinguir la menor
        self.frontera = []

        # contador utilizado para desempatar elementos de la cola de prioridad
        self.contador = 0 #inicia en 0 por ser la primera celda

        heuristica_inicial = (
            distancia_manhattan(posicion_inicial, self.mapa)
        )

        # se obtiene la celda correspondiente a la posicion inicial
        x, y = posicion_inicial
        celda_inicial = mapa[x][y]

        # se agrega el elemento: (f, g, contador, celda, posicion)
        # siguiendo el orden de una cola de prioridad
        heapq.heappush(
            self.frontera,
            (

                # funcion costo total: heuristica + costo_inicial
                heuristica_inicial, #iniciada como h al ser el costo acumulado 0

                0, #costo acumulado

                self.contador,  #para que al sacar un elemento de la pq habiendo
                #dos elementos con mismo costo acumulado y heuristica, se elija el
                #que tenga menor contador en vez de tener que comparar la celda,
                #el cual es el siguiente elemento de la tupla

                celda_inicial, #celda

                posicion_inicial #posicion

            )
        )

        self.contador += 1

        self.explorados = []

        self.posicion_actual = posicion_inicial

        # se agrega el agente a la celda inicial
        x, y = self.posicion_actual
        mapa[x][y].agentes.append(self)


def iterar_a_estrella(agente):

    # se comprueba si el agente ha sido alcanzado por el fuego
    alcanzado_por_fuego = efecto_fuego(agente)

    if alcanzado_por_fuego:
        return

    # si no quedan posiciones por terminar el agente se da por muerto
    # (no consiguio escapar dado que el fuego bloqueo la salida)
    # y la iteracion termina
    if not agente.frontera:
        agente.finalizado = True
        agente.vivo = False

        # se elimina de su celda actual
        x, y = agente.posicion_actual
        agente.mapa[x][y].agentes.remove(agente)

        return

    numero_random = random.randint(1, 100)

    # con baja probabilidad el agente ejecuta la accion de pasar por el turno (esperar)

    if numero_random <= 5:
        return

    # se saca la tupla (casilla) de la frontera con menor costo
    mejor_casilla = heapq.heappop(agente.frontera)

    f, costo_acumulado, _, nueva_celda, nueva_posicion= mejor_casilla

    # si la posicion ya fue explorada se ignora esta ruta
    if nueva_posicion in agente.explorados:
        return

    # el agente se mueve a la celda de la frontera con menor costo
    mover(agente, nueva_posicion)

    # se comprueba si encontro la salida
    escapo = escapar(agente)

    if escapo:
        return

    # se inserta en explorados
    agente.explorados.append(nueva_posicion)

    x, y = agente.posicion_actual

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    # se buscan vecinos nuevos los cuales poder explorar
    for dx, dy in movimientos:

        nueva_x = x + dx
        nueva_y = y + dy

        # se comprueba que este dentro del mapa
        if (0 <= nueva_x < len(agente.mapa)
                and 0 <= nueva_y < len(agente.mapa[0])):

            nueva_posicion = (nueva_x, nueva_y)
            nueva_celda = agente.mapa[nueva_x][nueva_y]

            # se comprueba que sea una posicion valida y no descubierta
            if (not nueva_celda.fuego
                    and not nueva_celda.muro
                    and nueva_posicion not in agente.explorados):

                # se obtiene el costo estimado a la salida de la posicion vecina
                heuristica = distancia_manhattan(
                    nueva_posicion,
                    agente.mapa
                )

                # se obtiene el costo acumulado desde el origen hasta la celda vecina
                costo_nuevo = costo_acumulado + nueva_celda.costo

                # se agrega la nueva celda a la frontera
                heapq.heappush(
                    agente.frontera,
                    (
                        costo_nuevo + heuristica,
                        costo_nuevo,
                        agente.contador,
                        nueva_celda,
                        nueva_posicion
                    )
                )

                agente.contador += 1



