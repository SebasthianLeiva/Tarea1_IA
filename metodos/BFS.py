
from collections import deque
from metodos.general.agente import *

class Agente_BFS:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        # cola de posiciones que BFS todavia debe explorar
        self.cola = deque()
        self.cola.append(posicion_inicial)

        # posiciones que ya fueron descubiertas
        self.descubiertos = set()
        self.descubiertos.add(posicion_inicial)

        self.posicion_actual = posicion_inicial

        # se agrega el agente a la celda inicial

        x, y = self.posicion_actual
        mapa[x][y].agentes.append(self)



def iterar_BFS(agente):

    #se comprueba si el agente ha sido alcanzado por el fuego
    alcanzado_por_fuego = efecto_fuego(agente)

    if alcanzado_por_fuego == True:
        return


    while agente.cola:

        # se saca la siguiente posicion de la cola
        x, y = agente.cola.popleft()

        nueva_celda = agente.mapa[x][y]

        # la posicion pudo incendiarse mientras estaba en la cola
        if nueva_celda.fuego:
            continue

        break

    # si no quedan posiciones por terminar el agente se da por muerto (no consiguio escapar
    # dado que el fuego bloqueo la salida) y la iteracion termina

    else:
        agente.finalizado = True
        agente.vivo = False

        #se elimina de su celda actual

        x, y = agente.posicion_actual
        agente.mapa[x][y].agentes.remove(agente)

        return


    #se actualiza la posicion del agente, se agrega a la nueva celda y se elimina de la
    #anterior
    mover(agente,(x,y))


    # se comprueba si el agente encontro la salida
    escapo = escapar(agente)

    if escapo == True:
        return



    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    for dx, dy in movimientos:

        nueva_x = x + dx
        nueva_y = y + dy

        # se verifica que este dentro del mapa
        if (0 <= nueva_x < len(agente.mapa) and 0 <= nueva_y < len(agente.mapa[0])):

            nueva_posicion = (nueva_x, nueva_y)
            nueva_celda = agente.mapa[nueva_x][nueva_y]

            # no entrar a fuego, muros ni posiciones ya visitadas
            if (not nueva_celda.fuego and not nueva_celda.muro
                    and nueva_posicion not in agente.descubiertos):

                agente.descubiertos.add(nueva_posicion)
                agente.cola.append(nueva_posicion)









