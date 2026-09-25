
import random
from metodos.general.agente import *
import copy
from metodos.general.fuego import Fuego, iteracionFuego

class Agente_genetico:

    def __init__(self, mapa, posicion_inicial):

        self.mapa = mapa
        self.posicion_actual = posicion_inicial

        self.finalizado = False
        self.vivo = True

        # cromosoma
        self.movimientos = []
        #300 movimientos para cada agente
        inicializar_movimientos(self.movimientos, 300)

        self.pos_movimientos = 0

        # calidad del cromosoma
        self.fitness = 0




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

#itera 10 veces obtener_geneticos() para retornar los 5 mejores agentes resultantes de
# las 10 generaciones

def obtener_generacion_final(mapa):

    padres = obtener_geneticos(mapa,[])

    generacion = 1

    while generacion !=11:

        hijos = obtener_geneticos(mapa,padres)
        padres = hijos
        generacion+=1

    padres.sort(key=lambda agente: agente.fitness, reverse=True)

    return padres[:5]




#retorna una generacion de 100 agentes resultantes del algoritmo genetico
def obtener_geneticos(mapa, padres):

    agentes = padres

    if(len(padres) == 0): #si es la primera generacion se crean los padres

        columnas = obtener_columnas()

        i = 0
        while i != 100:
            agentes.append(Agente_genetico(mapa, (29, columnas[i])))
            i += 1


    #se obtienen los 20 agentes con mejor fitness
    agentes_seleccionados = seleccion(agentes)

    #se obtienen 80 hijos salidos de la cruza de los 20 agentes con mejor fitness
    hijos = crossover(agentes_seleccionados)

    #con baja probabilidad se muta a algunos de los hijos
    mutacion(hijos)

    #se recalcula el fitness de los hijos
    for hijo in hijos:
        hijo.fitness = fitness(mapa,hijo)

    # se agregan los 20 mejores padres a los hijos tambien (para no perder buenos agentes)
    j = 0
    while j != 20:
        hijos.append(agentes_seleccionados[j])
        j += 1

    return hijos




#evalua un agente haciendo que itere sobre un mapa con fuego
def fitness(mapa, agente):
    # se genera un mapa diferente para cada agente
    mapa_prueba = copy.deepcopy(mapa)

    # Los mismos focos para todos los individuos
    fuegos = [
        Fuego(mapa_prueba, (29, 0)),
        Fuego(mapa_prueba, (29, 29))
    ]

    ####

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

    contador_fuego = 0  # el fuego se propaga al llegar a 4

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
            contador_fuego += 1
            if contador_fuego == 4:
                for fuego in fuegos:
                    iteracionFuego(fuego)

                contador_fuego = 0

                # Si el fuego alcanzo la posición del agente
                if mapa_prueba[posicion[0]][posicion[1]].fuego:
                    penalizacion += 100
                    agente.fitness = -1000 - penalizacion
                    return agente.fitness

            continue

        celda = mapa_prueba[nueva_x][nueva_y]

        # movimiento hacia un muro
        if celda.muro:
            penalizacion += 10
            contador_fuego += 1
            if contador_fuego == 4:
                for fuego in fuegos:
                    iteracionFuego(fuego)

                contador_fuego = 0

                # Si el fuego alcanzo la posición del agente
                if mapa_prueba[posicion[0]][posicion[1]].fuego:
                    penalizacion += 100
                    agente.fitness = -1000 - penalizacion
                    return agente.fitness

            continue

        # movimiento hacia el fuego
        if celda.fuego:
            penalizacion += 20
            contador_fuego += 1
            if contador_fuego == 4:
                for fuego in fuegos:
                    iteracionFuego(fuego)

                contador_fuego = 0

                # Si el fuego alcanzo la posicion del agente
                if mapa_prueba[posicion[0]][posicion[1]].fuego:
                    penalizacion += 100
                    agente.fitness = -1000 - penalizacion
                    return agente.fitness

            continue

        # movimiento valido
        posicion = nueva_posicion

        # si llego a la salida
        if celda.salida:
            agente.fitness = 1000 - penalizacion
            return agente.fitness

        contador_fuego += 1

        # Cada 4 movimientos se propaga el fuego
        if contador_fuego == 4:
            for fuego in fuegos:
                iteracionFuego(fuego)

            contador_fuego = 0

            # Si el fuego alcanzo la posición del agente
            if mapa_prueba[posicion[0]][posicion[1]].fuego:
                penalizacion += 100
                agente.fitness = -1000 - penalizacion
                return agente.fitness

    # si no llego a la salida, mientras mas cerca quede mejor
    distancia = abs(posicion[0] - salida[0]) + abs(posicion[1] - salida[1])

    agente.fitness = 100 - distancia - penalizacion

    return agente.fitness




#de la lista de agentes se elijen los 10 con mejor fitness
def seleccion(lista_agentes):

    lista_agentes.sort(key=lambda agente: agente.fitness, reverse=True)

    return lista_agentes[:20]



def crossover(lista_padres):

    hijos = []

    for i in range(0,80):
        padre1, padre2 = random.sample(lista_padres, 2) #se elijen 2 distintos

        numero = random.randint(1, 3)

        if numero==1:

            #el hijo adquiere los 40 primeros movimientos del padre 1 y el resto del
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1,padre2,100))

        elif numero==2:
            # el hijo adquiere los primeros 60 del 1 y el resto del 2
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1,padre2,150))

        elif numero == 3:
            # el hijo adquiere los primeros 80 del 1 y el resto del 2
            # padre 2 y es insertado en la lista de hijos
            hijos.append(generar_hijo(padre1, padre2, 200))

    return hijos




#coloca parte de los movimientos de ambos padres en el hijo y lo retorna
def generar_hijo(padre1, padre2, cant_padre1):

    columnas = obtener_columnas()
    i = random.randint(0, len(columnas)-1)

    posicion_inicial = (29, columnas[i])

    hijo = Agente_genetico(padre1.mapa, posicion_inicial)

    mitad_padre1 = padre1.movimientos[:cant_padre1]
    mitad_padre2 = padre2.movimientos[cant_padre1:]

    hijo.movimientos = mitad_padre1 + mitad_padre2

    return hijo



def mutacion(lista_hijos):

    movimientos_posibles = ["arriba","abajo","izquierda","derecha"]

    for hijo in lista_hijos:

        # 20% de probabilidad de que este hijo mute
        if random.random() < 0.20:

            # se elije que movimiento cambiar
            posicion = random.randint(0, len(hijo.movimientos) - 1)

            # se elije el nuevo movimiento
            nuevo_movimiento = random.choice(movimientos_posibles)

            hijo.movimientos[posicion] = nuevo_movimiento







def inicializar_movimientos(lista_movs,cantidad_movimientos):
    movimientos = [
        "arriba",
        "izquierda",
        "derecha",
        "abajo"
    ]

    i = 0

    while i < cantidad_movimientos:

        #se agrega un movimiento aleatorio de "movimientos" a la lista_movs
        numero = random.randint(0, 3)
        lista_movs.append(movimientos[numero])

        i += 1





#retorna columans de posicion inicial para los 100 agentes
def obtener_columnas():

    columnas = []

    while len(columnas) != 100:

        columna = random.randint(2, 28)
        columnas.append(columna)

    return columnas