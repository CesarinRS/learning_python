"""
Day 8 exercize from course: Python Total
"""

def turno_p():
    for n in range(1, 1000):
        yield f"P - {n}"

def turno_m():
    for n in range(1, 1000):
        yield f"M - {n}"

def turno_c():
    for n in range(1, 1000):
        yield f"C - {n}"

p = turno_p()
m = turno_m()
c = turno_c()


def decorador(area):

    print("\n" + "*" * 15)
    print("Su numero es: ")
    if area == 'P':
        print(next(p))
    elif area == 'M':
        print(next(m))
    else:
        print(next(c))
    print("En un momento sera atendido")
    print("\n" + "*" * 15)

def ask_client():

    print("Bienvenido a este receptor de clientes")

    while True:
        print("[P] - Perfumeria\n[M] - Medicamento\n[C] - Cosmeticos")
        try:
            option = input("Eliga su área de destino").upper()
            ['P','M','C'].index(option)
        except ValueError:
            print("Invalid option")
        else:
            break

    decorador(option)

def inicio():

    while True:
        ask_client()
        try:
            other_turn = input("Quieres sacar otro turno? [S] [N]").upper()
            ["S","N"].index(other_turn)
        except ValueError:
            print("Invalid option")
        else:
            if other_turn == 'N':
                print("Thanks for use this app")
                break

inicio()



