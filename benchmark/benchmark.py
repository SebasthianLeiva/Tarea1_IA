#falta el import a simulador

from mapas.mapas import *


def benchmark():

    #TODO: ejecutar las 80/200 iteraciones de la simulacion para cada
    # par metodo y mapa, luego obtener metricas a partir de los datos

    mapa = obtener_mapa(alta_densidad())

    imprimir_matriz(mapa)


    #simulacion(alta_densidad(),Metodo.COSTO_UNIFORME)  #simulacion de costo uniforme


    return