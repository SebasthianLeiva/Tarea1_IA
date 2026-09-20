
from mapas.mapas import *

from metodos.fuego import *
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



def simulacion(matriz,metodo):

    mapa = obtener_mapa(matriz) #mapa de celdas

    agente,iteracion = obtener_metodo(metodo)

    if agente != Agente_genetico:
        posiciones_y = obtener_columnas()  #posiciones en y de los agentes

        agentes = []  # lista de agentes

        for i in range(5):  # se insertan los 5 agentes en la lista
            agentes.append(agente(mapa, (29, posiciones_y[i])))

    else:
        agentes = obtener_geneticos(mapa)


    #4 focos de fuego

    fuegos = []

    for i in range(5): #se insertan los 5 focos de fuego en la lista
        fuegos.append(Fuego(mapa,(random.randint(2, 27), random.randint(2, 27))))


    # lleva la cuenta de la cantidad de turnos que ha durado la simulacion

    turnos_simulacion = 1

    turnos_fuego = 3

    #ciclo de la simulacion
    while True:

        print("\n##############################", flush=True)

        print("turno: " , turnos_simulacion)


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


        #se cuenta la cantidad de agentes finalizados, si finalizaron los 5
        #la simulacion termina

        numero_finalizados = 0

        #cantidad de agentes que lograron escapar

        numero_supervivientes = 0

        for agente in agentes:

            if agente.finalizado == True:

                numero_finalizados+=1

                if agente.vivo == True:

                    numero_supervivientes+=1


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

        if numero_finalizados == 5:

            return numero_supervivientes, turnos_simulacion

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






    #TODO: añadir los casos de los demas metodos


    #case Metodo.A_ESTRELLA:
    #    return AgeneA_ESTRELLA, iterarA_ESTRELLA




# retorna una lista con las posiciones de inicio de los 5 agentes,
# de esta forma no se repiten posiciones y hay variacion en el
# comportamiento de los algoritmos

def obtener_columnas():

    columnas = []

    while len(columnas) != 5:

        columna = random.randint(2, 28)

        if columna not in columnas:
                columnas.append(columna)

    return columnas




