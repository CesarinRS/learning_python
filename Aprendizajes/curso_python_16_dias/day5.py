"""
Dia 5 del curso 16 dias
Proyecto: juego del ahorcado
"""
from random import *

lifes = 6
lista_palabras = ["nuevo","calendario","carne","anime","netflix","carro","cocina","canal","cuerno"]
palabra = choice(lista_palabras)
user = input("Ingresa tu nombre porfavor: ")

print(f"Bienvenido, {user} \n Tienes 6 vidas para completar la frase, por cada letra incorrecta perderas una vida\n"
      f"Puedes imaginar que palabra es por la cantidad de guiones (una letra = un guion). \nBuena suerte, jugador!")

def ocultar_palabra(palabra):
    return "-" * len(palabra)

def actualizar_palabra(palabra, oculta, letra):
    nueva_oculta = list(oculta)
    for i, l in enumerate(palabra):
        if l == letra:
            nueva_oculta[i] = letra
    return "".join(nueva_oculta)

oculta = ocultar_palabra(palabra)
print(f"Palabra: {oculta}")

while lifes > 0 and "-" in oculta:
        user_option = input("Selecciona una letra porfavor: ").lower()

        if len(user_option) != 1 or not user_option.isalpha():
            print("Ingreso invalido. Porfavor ingresa solo una letra.")
            continue
        if user_option in palabra:
            oculta = actualizar_palabra(palabra, oculta, user_option)
            print(f"Buen trabajo! Sigue así {oculta}")
        else:
            lifes -= 1
            print(f"Mala elección! Te restan {lifes} {'lives' if lifes > 1 else 'life'} Vidas.")
if "-" not in oculta:
    print(f"\nFelicidades {user}! Has ganado! La palabra oculta era: '{palabra}'.")

else:
    print(f"\nEl juego a acabado, {user}! Buena suerte en la proxima! La palabra oculta era: '{oculta}'.")