
import heapq

from .agente import *
from .distancia_manhattan import distancia_manhattan

from mapas import mapas


class Agente_greedyBFS:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        # frontera
        self.frontera = []

        heuristica_inicial = (distancia_manhattan(posicion_inicial,self.mapa))

        #se agrega el elemento: posicion,heuristica a la frontera siguiendo el orden
        #de una cola de prioridad

        heapq.heappush(
            self.frontera,
            (heuristica_inicial, posicion_inicial)
        )

        self.explorados = []

        self.posicion_actual = posicion_inicial

        # se agrega el agente a la celda inicial
        x, y = self.posicion_actual
        mapa[x][y].agentes.append(self)







def iterar_greedyBFS(agente):

    # se comprueba si el agente ha sido alcanzado por el fuego
    alcanzado_por_fuego = efecto_fuego(agente)

    if alcanzado_por_fuego:
        return

    # si no quedan posiciones por terminar el agente se da por muerto (no consiguio escapar
    # dado que el fuego bloqueo la salida) y la iteracion termina

    if not agente.frontera:
        agente.finalizado = True
        agente.vivo = False

        # se elimina de su celda actual

        x, y = agente.posicion_actual
        agente.mapa[x][y].agentes.remove(agente)

        return

    # se saca el nodo de la frontera con menor heuristica
    mejor_nodo = heapq.heappop(agente.frontera)

    # el agente se mueve al nodo de la frontera con menor heuristica
    heuristica,nueva_posicion, = mejor_nodo
    mover(agente, nueva_posicion)

    # se comprueba si encontró la salida
    escapo = escapar(agente)

    if escapo:
        return

    #se inserta en explorados
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

        # comprobar que este dentro del mapa
        if (0 <= nueva_x < len(agente.mapa)
                and 0 <= nueva_y < len(agente.mapa[0])):

            nueva_posicion = (nueva_x, nueva_y)
            nueva_celda = agente.mapa[nueva_x][nueva_y]

            # comprobar que sea una posicion valida y no descubierta
            if (not nueva_celda.fuego
                    and not nueva_celda.muro
                    and nueva_posicion not in agente.explorados):

                    #se obtiene el costo estimado a la salida de la posicion vecina
                    heuristica = distancia_manhattan(nueva_posicion,agente.mapa)


                    #si es que el elemento no esta ya en la frontera se inserta
                    if not any(posicion == nueva_posicion for _
                    , posicion in agente.frontera):

                        heapq.heappush(
                            agente.frontera,
                            (heuristica, nueva_posicion)
                        )




