"""
Archivo para definir generadores y decoradores que se utilizaran en el main
"""


def decorar_impresion(funcion):

    def wrapper(*args, **kwargs):
        for turno in funcion(*args, **kwargs):
            print("Hola estimado usuario, su turno es:")
            print(turno)
            print("Por favor, aguarde hasta que lo llamen")
            yield turno
    return wrapper


@decorar_impresion
def contador():
    turno = 1
    while True:
        yield f"El número {turno}"
        turno += 1


contador_perfumes = contador()
contador_medicamentos = contador()
contador_cosmetologia = contador()

