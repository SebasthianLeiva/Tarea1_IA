

import heapq

class Agente_CU:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.finalizado = False
        self.vivo = True

        #
        #listas
        #

        self.cola = heapq()

        self.posicion_actual = posicion_inicial

        # se agrega el agente a la celda inicial

        x, y = self.posicion_actual
        mapa[x][y].agentes.append(self)



#una iteracion del metodo costo uniforme

def iterar_CU():

    print()



