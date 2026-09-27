
from benchmark.benchmark import *
from benchmark.simulador import *
from benchmark.simulador import Metodo
from mapas.mapas import *


def main():

   mapas = {
      "1": alta_densidad,
      "2": densidad_media,
      "3": baja_densidad
   }

   metodos = {
      "1": Metodo.BFS,
      "2": Metodo.DFS,
      "3": Metodo.GREEDY_BFS,
      "4": Metodo.A_ESTRELLA,
      "5": Metodo.GENETICO
   }

   while True:

      print("\nOpciones:\n1. Ejecutar benchmark")
      print("2. Ejecutar simulación individual")
      print("3. Salir")

      opcion = input("\nSeleccionar opcion: ")

      if(opcion == "1"):
         benchmark()

      elif (opcion == "2"):

         print("\nMapas: \n1. Alta densidad\n2. Densidad media\n3. Baja densidad")

         opcion_mapa = input("\nSeleccionar mapa: ")

         if(opcion_mapa=="1"):
            mapa = alta_densidad()

         elif (opcion_mapa == "2"):
            mapa = densidad_media()

         elif (opcion_mapa == "3"):
            mapa = baja_densidad()


         print("\nMetodos: \n1.BFS\n2.DFS\n3.Greedy_BFS\n4.A*\n5.Genetico")

         opcion_metodo = input("\nSeleccionar metodo: ")

         mapa = mapas[opcion_mapa]()
         metodo = metodos[opcion_metodo]

         print("")

         simulacion(mapa, metodo, True)


      elif opcion == "3":
         break



main()



