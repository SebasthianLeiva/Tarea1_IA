
#heuristica para greedy_BFS y A*

def distancia_manhattan(posicion_celda, mapa):

    salida = obtener_salida(mapa)

    x1, y1 = posicion_celda
    x2, y2 = salida

    return abs(x1 - x2) + abs(y1 - y2)


def obtener_salida(mapa):

    for x in range(len(mapa)):
        for y in range(len(mapa[0])):

            if mapa[x][y].salida:
                return x, y