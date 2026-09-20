
import random
from mapas.mapas import *
from .agente import *

class Agente_genetico:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.posicion_actual = posicion_inicial

        self.finalizado = False
        self.vivo = True

        # cromosoma
        self.movimientos = []
        inicializar_movimientos(self.movimientos, 60)

        self.pos_movimientos = 0

        # calidad del individuo
        self.fitness = fitness(self.mapa,self)




def iterar_genetico(agente):

    # se comprueba si el agente ha sido alcanzado por el fuego
    alcanzado_por_fuego = efecto_fuego(agente)

    if alcanzado_por_fuego == True:
        return

    # se obtiene la posicion correspondiente al siguiente movimiento
    movimiento = agente.movimientos[agente.pos_movimientos]

    x, y = agente.posicion_actual

    # se determina la nueva posicion dependiendo del movimiento
    if movimiento == "arriba":
        nueva_posicion = (x - 1, y)

    elif movimiento == "abajo":
        nueva_posicion = (x + 1, y)

    elif movimiento == "izquierda":
        nueva_posicion = (x, y - 1)

    elif movimiento == "derecha":
        nueva_posicion = (x, y + 1)

    elif movimiento == "esperar":
        nueva_posicion = (x, y)

    nueva_x, nueva_y = nueva_posicion

    # se comprueba si la nueva posicion esta dentro del mapa
    if (0 <= nueva_x < len(agente.mapa)
            and 0 <= nueva_y < len(agente.mapa[0])):

        nueva_celda = agente.mapa[nueva_x][nueva_y]

        # se comprueba que la celda no sea un muro ni fuego
        if not nueva_celda.muro and not nueva_celda.fuego:

            # se actualiza la posicion del agente
            mover(agente, nueva_posicion)

            # se comprueba si el agente encontro la salida
            escapo = escapar(agente)

            if escapo == True:
                return

    # aunque el movimiento sea invalido, el turno se consume
    agente.pos_movimientos += 1

    # si ya ejecuto todos los movimientos se da por muerto y termina
    if agente.pos_movimientos >= len(agente.movimientos):

        agente.finalizado = True
        agente.vivo = False

        # se elimina de su celda actual

        x, y = agente.posicion_actual
        agente.mapa[x][y].agentes.remove(agente)

        return





#retorna 5 agentes resultantes del algoritmo genetico
def obtener_geneticos(mapa):

    agentes = []
    columnas = obtener_columnas()

    i=0
    while i!= 100:
        agentes.append(Agente_genetico(mapa,(29,columnas[i])))
        i+=1

    #se obtienen los 10 agentes con mejor fitness
    agentes_seleccionados = seleccion(agentes)

    #se obtienen 5 hijos salidos de la cruza de los 10 agentes con mejor fitness
    hijos = crossover(agentes_seleccionados)

    #con baja probabilidad se muta a algunos de los hijos
    mutacion(hijos)

    return hijos




#evalua un agente
def fitness(mapa, agente):

    posicion = agente.posicion_actual
    penalizacion = 0

    # encontrar la salida
    salida = None

    for x in range(len(mapa)):
        for y in range(len(mapa[0])):
            if mapa[x][y].salida:
                salida = (x, y)
                break

        if salida is not None:
            break

    # simular los movimientos
    for movimiento in agente.movimientos:

        x, y = posicion

        if movimiento == "arriba":
            nueva_posicion = (x - 1, y)

        elif movimiento == "abajo":
            nueva_posicion = (x + 1, y)

        elif movimiento == "izquierda":
            nueva_posicion = (x, y - 1)

        elif movimiento == "derecha":
            nueva_posicion = (x, y + 1)

        elif movimiento == "esperar":
            nueva_posicion = posicion

        nueva_x, nueva_y = nueva_posicion

        # movimiento fuera del mapa
        if not (0 <= nueva_x < len(mapa)
                and 0 <= nueva_y < len(mapa[0])):

            penalizacion += 10
            continue

        celda = mapa[nueva_x][nueva_y]

        # movimiento hacia un muro
        if celda.muro:
            penalizacion += 10
            continue

        # movimiento hacia el fuego
        if celda.fuego:
            penalizacion += 20
            continue

        # movimiento válido
        posicion = nueva_posicion

        # si llego a la salida
        if celda.salida:
            agente.fitness = 1000 - penalizacion
            return agente.fitness

    # si no llego a la salida, mientras más cerca quede mejor
    distancia = abs(posicion[0] - salida[0]) + abs(posicion[1] - salida[1])

    agente.fitness = 100 - distancia - penalizacion

    return agente.fitness





#de la lista de agentes se elijen los 10 con mejor fitness
def seleccion(lista_agentes):

    lista_agentes.sort(key=lambda agente: agente.fitness, reverse=True)

    return lista_agentes[:10]



def crossover(lista_padres):

    hijos = []

    for i in range(0,5):
        padre1, padre2 = random.sample(lista_padres, 2) #se elijen 2 distintos

        numero = random.randint(1, 3)

        if numero==1:

            #el hijo adquiere los 20 primeros movimientos del padre 1 y los 40 ultimos del
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1,padre2,20))

        elif numero==2:
            # el hijo adquiere los primeros 30 del 1 y el resto del 2
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1,padre2,30))

        elif numero == 3:
            # el hijo adquiere los primeros 40 del 1 y el resto del 2
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1, padre2, 40))

    return hijos




#coloca parte de los movimientos de ambos padres en el hijo y lo retorna
def generar_hijo(padre1, padre2, cant_padre1):

    hijo = Agente_genetico(padre1.mapa, (padre1.posicion_actual))

    mitad_padre1 = padre1.movimientos[:cant_padre1]
    mitad_padre2 = padre2.movimientos[cant_padre1:]

    hijo.movimientos.extend(mitad_padre1)
    hijo.movimientos.extend(mitad_padre2)

    # se agrega el agente a su celda inicial del mapa
    x, y = padre1.posicion_actual
    hijo.mapa[x][y].agentes.append(hijo)

    return hijo


def mutacion(lista_hijos):

    movimientos_posibles = ["arriba","abajo","izquierda","derecha","esperar"]

    for hijo in lista_hijos:

        # 20% de probabilidad de que este hijo mute
        if random.random() < 0.20:

            # se elije que movimiento cambiar
            posicion = random.randint(0, 59)

            # se elije el nuevo movimiento
            nuevo_movimiento = random.choice(movimientos_posibles)

            hijo.movimientos[posicion] = nuevo_movimiento







def inicializar_movimientos(lista_movs,cantidad_movimientos):

    i = 0
    while i < cantidad_movimientos:

        numero = random.randint(1, 5)

        if numero==1:
            lista_movs.append("arriba")

        elif numero==2:
            lista_movs.append("izquierda")

        elif numero==3:
            lista_movs.append("derecha")

        elif numero==4:
            lista_movs.append("abajo")

        elif numero==5:
            lista_movs.append("esperar")

        i+=1


#retorna columans de posicion inicial para los 100 agentes
def obtener_columnas():

    columnas = []

    while len(columnas) != 100:

        columna = random.randint(2, 28)
        columnas.append(columna)

    return columnas