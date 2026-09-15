
from mapas.mapas import *

from metodos.costo_uniforme import *

from enum import Enum
import random



class Metodo(Enum):
    BFS= 1
    COSTO_UNIFORME = 2
    GREEDY_BFS= 3
    A_ESTRELLA = 4
    GENETICO = 5



def simulacion(matriz,metodo):

    mapa = obtener_mapa(matriz) #mapa de celdas

    agente,iteracion = obtener_metodo(metodo)

    posiciones_y = obtener_columnas()  #posiciones en y de los agentes


    agentes = [agente(mapa,(29,posiciones_y[0])), agente(mapa, (29, posiciones_y[1])),
               agente(mapa, (29, posiciones_y[2])), agente(mapa, (29, posiciones_y[3])),
               agente(mapa, (29, posiciones_y[4]))]


    #ciclo de la simulacion

    while True:

        iteracion(agentes[0])
        iteracion(agentes[1])
        iteracion(agentes[2])
        iteracion(agentes[3])
        iteracion(agentes[4])

        imprimir_matriz(mapa)

        numero_finalizados = 0

        for agente in agentes:

            if agente.finalizado == True:

                numero_finalizados+=1

        if numero_finalizados == 5:

            return




def obtener_metodo(metodo):

    match metodo:

        case Metodo.COSTO_UNIFORME:

            return AgenteCU,iterarCU



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




