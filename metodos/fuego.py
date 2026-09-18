

from collections import deque


class Fuego:

    def __init__(self, mapa, inicio):
        self.mapa = mapa
        self.cola = deque()
        self.descubiertos = set()

        self.cola.append(inicio)
        self.descubiertos.add(inicio)

        # posicion actual del frente del fuego

        self.posicion_actual = inicio


def iteracionFuego(fuego):

    if not fuego.cola:
        return

    posicion = fuego.cola.popleft()

    fuego.posicion_actual = posicion

    x, y = posicion

    # La celda que alcanza el fuego queda consumida
    fuego.mapa[x][y].fuego = True

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    for dx, dy in movimientos:

        nueva_x = x + dx
        nueva_y = y + dy

        #se comprueba unicamente que el fuego este dentro del mapa

        if (0 <= nueva_x < len(fuego.mapa)
                and 0 <= nueva_y < len(fuego.mapa[0])):

            nueva_posicion = (nueva_x, nueva_y)

            if nueva_posicion not in fuego.descubiertos:

                fuego.descubiertos.add(nueva_posicion)
                fuego.cola.append(nueva_posicion)