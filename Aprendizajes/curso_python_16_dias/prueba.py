"""
This script is available for practices
"""

def decorador_saludo(funcion):
    print("Buenas tardes, su turno es:")
    funcion()
    print("Porfavor espere su turno")

def generador_turnos():
    turno = 1
    while True:
        yield turno
        turno += 1

def sesion():

    perfumes = generador_turnos()
    medicamentos = generador_turnos()
    cosmetologia = generador_turnos()

    eleccion = input("Ingrese una opción para imprimir su ticket: \n'P' turno en área de perfumes\n'M' turno en área de medicamentos\n'C' turno en área de cósmeticos").lower()

    def impresion_turno(eleccion):
        return f"{eleccion.upper()}"


    while eleccion == 'p':

        decorador_saludo(impresion_turno(eleccion))
        next(perfumes)
        print(f"{eleccion.upper()} - {perfumes}")


        if eleccion == 'm':
            decorador_saludo(impresion_turno(eleccion))
            next(medicamentos)
            print(f"{eleccion.upper()} - {medicamentos}")


        elif eleccion == 'c':
            decorador_saludo(impresion_turno(eleccion))
            next(cosmetologia)
            print(f"{eleccion.upper()} - {cosmetologia}")


        else:
            break


sesion()
