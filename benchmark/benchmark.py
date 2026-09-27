
from benchmark.simulador import *

from mapas.mapas import *


import statistics


def benchmark():

    mapas = [
        ("alta_densidad", alta_densidad),
        ("densidad_media", densidad_media),
        ("baja_densidad", baja_densidad)
    ]

    metodos = [
        Metodo.BFS,
        Metodo.DFS,
        Metodo.GREEDY_BFS,
        Metodo.A_ESTRELLA,
        Metodo.GENETICO
    ]


    total_agentes = 80

    for nombre_mapa, mapa in mapas:

        for metodo in metodos:

            tasas_supervivencia = []
            tiempos = []

            for i in range(200):

                num_vivos, cant_turnos = simulacion(mapa(), metodo,False)

                # tasa de supervivencia de esta ejecucion
                tasa = num_vivos / total_agentes

                tasas_supervivencia.append(tasa)

                #se evita contar la cantidad de turnos cuando ningun agente sobrevive
                if(num_vivos> 0):
                    tiempos.append(cant_turnos)

            # estadisticos de supervivencia
            media_supervivencia = statistics.mean(tasas_supervivencia)
            desviacion_supervivencia = statistics.stdev(tasas_supervivencia)
            minimo_supervivencia = min(tasas_supervivencia)
            maximo_supervivencia = max(tasas_supervivencia)

            # estadisticos de tiempo

            if len(tiempos) == 0:

                media_tiempo = None
                desviacion_tiempo = None
                minimo_tiempo = None
                maximo_tiempo = None

            elif len(tiempos) == 1:

                media_tiempo = statistics.mean(tiempos)
                desviacion_tiempo = None
                minimo_tiempo = min(tiempos)
                maximo_tiempo = max(tiempos)

            else:

                media_tiempo = statistics.mean(tiempos)
                desviacion_tiempo = statistics.stdev(tiempos)
                minimo_tiempo = min(tiempos)
                maximo_tiempo = max(tiempos)


            print("\n====================================")
            print("mapa:", nombre_mapa)
            print("metodo:", metodo.name)
            print("====================================")

            print(f"supervivencia promedio: {media_supervivencia:.3f}" )
            print(f"supervivencia desviación estandar: {desviacion_supervivencia:.3f}")
            print("supervivencia minimo :", minimo_supervivencia)
            print("supervivencia maximo :", maximo_supervivencia)

            if len(tiempos) == 0:

                print("tiempo promedio: N/A")
                print("tiempo desviación estandar: N/A")
                print("tiempo minimo: N/A")
                print("tiempo maximo: N/A")

            elif len(tiempos) == 1:

                print(f"tiempo promedio: {media_tiempo:.3f}")
                print("tiempo desviación estandar: N/A")
                print(f"tiempo minimo: {minimo_tiempo}")
                print(f"tiempo maximo: {maximo_tiempo}")

            else:

                print(f"tiempo promedio: {media_tiempo:.3f}")
                print(f"tiempo desviación estandar: {desviacion_tiempo:.3f}")
                print(f"tiempo minimo: {minimo_tiempo}")
                print(f"tiempo maximo: {maximo_tiempo}")

    return

