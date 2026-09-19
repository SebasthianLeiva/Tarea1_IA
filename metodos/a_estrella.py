
import heapq

from .agente import *
from .distancia_manhattan import distancia_manhattan
import random

from mapas import mapas


class Agente_a_estrella:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        # frontera
        self.frontera = []

        # contador utilizado para desempatar elementos de la cola de prioridad
        self.contador = 0

        heuristica_inicial = (
            distancia_manhattan(posicion_inicial, self.mapa)
        )

        # se obtiene la celda correspondiente a la posicion inicial
        x, y = posicion_inicial
        celda_inicial = mapa[x][y]

        # se agrega el elemento:
        # f, g, contador, celda, posicion, padre
        # siguiendo el orden de una cola de prioridad
        heapq.heappush(
            self.frontera,
            (
                heuristica_inicial,
                0,
                self.contador,
                celda_inicial,
                posicion_inicial,
                -1
            )
        )

        self.contador += 1

        # diccionario que guarda el padre de los nodos explorados

        # el inicial no tiene padre por lo que el valor de su padre se coloca como
        # -1
        self.padres = {posicion_inicial: -1}

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
    #lo que permite que la casilla con menor funcion costo total se actualice al siguiente
    #en caso de descongestionarse la actual

    if numero_random <= 15:
        return

    # se saca el nodo de la frontera con menor costo
    mejor_nodo = heapq.heappop(agente.frontera)

    f, costo_acumulado, _, nueva_celda, nueva_posicion, padre = mejor_nodo

    # si la posicion ya fue explorada se ignora esta ruta
    if nueva_posicion in agente.explorados:
        return

    # se guarda el padre de la ruta que resulto ser la mejor
    agente.padres[nueva_posicion] = padre

    # el agente se mueve al nodo de la frontera con menor costo
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

                # se obtiene el costo acumulado desde el origen hasta el nodo vecino
                costo_nuevo = costo_acumulado + nueva_celda.costo

                # se agrega el nuevo nodo a la frontera
                # se guarda tambien el padre que corresponde a esta ruta
                heapq.heappush(
                    agente.frontera,
                    (
                        costo_nuevo + heuristica,
                        costo_nuevo,
                        agente.contador,
                        nueva_celda,
                        nueva_posicion,
                        agente.posicion_actual
                    )
                )

                agente.contador += 1



