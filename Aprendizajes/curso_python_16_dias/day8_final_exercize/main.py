"""
Programa principal, busca simular una interfaz de turnos, tendrá tres áreas; perfumes, medicamentos y
cosmetología.

Importaremos de numbers.py los generadores y los decoradores.

Ejercicio final del día 8 del curso Python en 16 días
"""
from .numbers import decorar_impresion, contador_perfumes, contador_medicamentos, contador_cosmetologia

try:
    while True:
        peticion_usuario = input("Ingrese área a la que desea sacar turno: \n\t1: Perfumes \n\t2: Medicamentos \n\t3: Cosmetología \n\t4: Salir" )

        if peticion_usuario == "1":
            next(contador_perfumes)

        elif peticion_usuario == "2":
            next(contador_medicamentos)

        elif peticion_usuario == "3":
            next(contador_cosmetologia)

        elif peticion_usuario == "4":
            print("Estimado usuario, gracias por visitar nuestra tienda, ¡Nos vemos pronto!")
            break

        else:
            print("Opción invalida, vuelve a intentarlo")
            continue
except Exception as error:
    print(f"A sucedido un error {error}")