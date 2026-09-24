

def mover(agente, nueva_posicion):

    x, y = agente.posicion_actual
    nueva_x, nueva_y = nueva_posicion

    # sacar al agente de su celda actual
    agente.mapa[x][y].agentes.remove(agente)

    # actualizar posición del agente
    agente.posicion_actual = nueva_posicion

    # agregarlo a la nueva celda
    agente.mapa[nueva_x][nueva_y].agentes.append(agente)



#comprueba si el fuego alcanzo al agente

def efecto_fuego(agente):

    x, y = agente.posicion_actual
    celda_actual = agente.mapa[x][y]

    # si el fuego alcanzo al agente su estado pasa a muerto, finalizado y se remueve
    #de su celda

    if celda_actual.fuego:
        agente.vivo = False
        agente.finalizado = True
        # se remueve el agente de la celda
        celda_actual.agentes.remove(agente)
        return True

    return False


#cambia el estado del agente a finalizado y remueve a este de su celda si es que encontro la
# salida

def escapar(agente):

    x,y = agente.posicion_actual

    celda_actual = agente.mapa[x][y]

    if celda_actual.salida:
        agente.finalizado = True
        #se remueve el agente de la celda
        celda_actual.agentes.remove(agente)

        return True

    return False


