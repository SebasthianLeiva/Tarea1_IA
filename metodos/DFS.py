
from .agente import *


class Agente_DFS:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        # camino que el agente esta siguiendo
        self.camino = [posicion_inicial]

        # posiciones que ya fueron descubiertas
        self.descubiertos = set()
        self.descubiertos.add(posicion_inicial)

        self.posicion_actual = posicion_inicial

        # se agrega el agente a la celda inicial
        x, y = self.posicion_actual
        mapa[x][y].agentes.append(self)







def iterar_DFS(agente):

    # se comprueba si el agente ha sido alcanzado por el fuego
    alcanzado_por_fuego = efecto_fuego(agente)

    if alcanzado_por_fuego:
        return

    # se comprueba si encontró la salida
    escapo = escapar(agente)

    if escapo:
        return

    x, y = agente.posicion_actual

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    # buscar un vecino nuevo al que avanzar
    for dx, dy in movimientos:

        nueva_x = x + dx
        nueva_y = y + dy

        # comprobar que este dentro del mapa
        if (0 <= nueva_x < len(agente.mapa)
                and 0 <= nueva_y < len(agente.mapa[0])):

            nueva_posicion = (nueva_x, nueva_y)
            nueva_celda = agente.mapa[nueva_x][nueva_y]

            # comprobar que sea una posicion valida y no descubierta
            if (not nueva_celda.fuego
                    and not nueva_celda.muro
                    and nueva_posicion not in agente.descubiertos):

                # se marca como descubierta
                agente.descubiertos.add(nueva_posicion)

                # se agrega al camino
                agente.camino.append(nueva_posicion)

                # se mueve una celda
                mover(agente, nueva_posicion)

                return


    # si llego aqui, no tiene vecinos nuevos entonces debe volver hacia atras

    # si solo queda la posicion inicial no hay ningun lugar mas al que retroceder por lo que
    #el agente se da por muerto

    if len(agente.camino) == 1:

        agente.finalizado = True
        agente.vivo = False

        x, y = agente.posicion_actual
        agente.mapa[x][y].agentes.remove(agente)

        return

    # sacar la posicion actual del camino
    agente.camino.pop()

    # la nueva ultima posicion es aquella a la que debe retroceder

    posicion_anterior = agente.camino[-1] #obtiene el ultimo elemento de la lista

    mover(agente, posicion_anterior)