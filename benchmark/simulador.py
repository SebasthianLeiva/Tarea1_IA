
from mapas.mapas import *

from metodos.general.fuego import *
from metodos.BFS import *
from metodos.DFS import*
from metodos.greedyBFS import*
from metodos.a_estrella import *
from metodos.genetico import *

from enum import Enum
import random




class Metodo(Enum):
    BFS= 1
    DFS = 2
    GREEDY_BFS= 3
    A_ESTRELLA = 4
    GENETICO = 5



def simulacion(matriz,metodo,imprimir):

    cant_agentes = 80

    mapa = obtener_mapa(matriz) #mapa de celdas

    agente,iteracion = obtener_metodo(metodo)

    if agente != Agente_genetico:

        posiciones = obtener_posiciones(mapa)

        agentes = []  # lista de agentes

        for i in range(cant_agentes):  # se insertan los 80 agentes en la lista
            agentes.append(agente(mapa, posiciones[i]))

    else:

        posiciones = obtener_posiciones(mapa)

        agentes = obtener_generacion_final(posiciones,mapa)

        #se colocan en el mapa
        for agente in agentes:
            x, y = agente.posicion_actual
            mapa[x][y].agentes.append(agente)


    fuegos = []

    #2 focos de fuego con las esquinas inferiores del mapa como pos_inicial
    fuegos.append(Fuego(mapa, (29, 0)))
    fuegos.append(Fuego(mapa, (29, 29)))



    # lleva la cuenta de la cantidad de turnos que ha durado la simulacion

    turnos_simulacion = 1

    #la cantidad de turnos que le tomo al ultimo superviviente escapar
    turnos_ultimo_superviviente = 0

    turnos_fuego = 3

    #guarda los agentes supervivientes y el turno en el que salieron en orden ascendente de
    # izquierda a derecha

    supervivientes = []

    #ciclo de la simulacion
    while True:

        if(imprimir == True):
            print("\n##############################", flush=True)

            print("turno: ", turnos_simulacion)


        if (turnos_fuego == 0):
            for fuego in fuegos: #cada foco de fuego hace una iteracion
                iteracionFuego(fuego)

            turnos_fuego = 3

        # cada agente hace una iteracion si es que su estado no esta finalizado
        for agente in agentes:

            if agente.finalizado == False:
                iteracion(agente)



        #la cantidad de turnos para la proxima propagacion del fuego disminuye en 1

        turnos_fuego-=1


        turnos_simulacion += 1


        #se cuenta la cantidad de agentes finalizados, si finalizaron los 80
        #la simulacion termina

        numero_finalizados = 0

        #cantidad de agentes que lograron escapar

        numero_supervivientes = 0

        for agente in agentes:

            if agente.finalizado == True:

                numero_finalizados+=1

                if agente.vivo == True:

                    numero_supervivientes+=1

                    if agente not in supervivientes:
                        supervivientes.append((agente,turnos_simulacion))

        if(imprimir==True):

            for i, agente in enumerate(agentes):
                print(
                    i,
                    "pos:", agente.posicion_actual,
                    "finalizado:", agente.finalizado,
                    "vivo:", agente.vivo
                )

            imprimir_matriz(mapa)

            print("\nnumero de agentes finalizados: " + str(numero_finalizados))

            print("numero de agentes supervivientes: " + str(numero_supervivientes) + "\n")



        if numero_finalizados == cant_agentes:

            if(supervivientes):
                # se retorna el numero de supervivientes y los turnos que le tomo al ultimo
                #salir
                return numero_supervivientes, supervivientes[-1][1]

            else:

                return 0, 0


        #input()





def obtener_metodo(metodo):

    match metodo:

        case Metodo.DFS:

            return Agente_DFS,iterar_DFS

        case Metodo.BFS:

            return Agente_BFS,iterar_BFS

        case Metodo.GREEDY_BFS:

            return Agente_greedyBFS,iterar_greedyBFS

        case Metodo.A_ESTRELLA:

            return Agente_a_estrella,iterar_a_estrella

        case Metodo.GENETICO:

            return Agente_genetico,iterar_genetico






#recorre el mapa de derecha a izquierda de abajo hacia arriba y retorna un arreglo con
# posiciones validas para que los agentes inicien

def obtener_posiciones(mapa):

    posiciones = []

    for i in range(len(mapa) - 1, -1, -1):
        for j in range(len(mapa[0]) - 1, -1, -1):

            if mapa[i][j].costo_base != 0 and mapa[i][j].costo_base != 6:
                posiciones.append((i, j))

                if len(posiciones) == 80:
                    return posiciones







