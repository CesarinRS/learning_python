from random import *


def lanzar_dados():
    dado1 = randint(1, 6)
    dado2 = randint(1, 6)
    return dado1, dado2


def evaluar_jugada(dado1, dado2):
    suma_dados = dado1 + dado2
    if suma_dados <= 6:
        return f"La suma de tus dados es {suma_dados}.\nLamentable"
    elif 7 <= suma_dados < 10:
        return f"La suma de tus dados es {suma_dados}.\nTienes buenas chances"
    else:
        return f"La suma de tus dados es {suma_dados}.\nParece una jugada ganadora"

