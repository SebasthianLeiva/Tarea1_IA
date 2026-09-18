
from benchmark.simulador import *

from mapas.mapas import *


def benchmark():

    #TODO: ejecutar las 80/200 iteraciones de la simulacion para cada
    # par metodo y mapa, luego obtener metricas a partir de los datos


    #se obtiene la cantidad de agentes vivos tras la simulacion, y la cantidad de turnos
    #que le tomo al ultimo escapar

    num_vivos, cant_turnos = simulacion(alta_densidad(),Metodo.DFS)  #simulacion de costo uniforme

    print("numero de agentes vivos: " + str(num_vivos ))
    print("cantidad de turnos totales: " + str(cant_turnos))


    return