"""
Proyecto del día 7
"""
from random import randint


class Persona:
    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

class Cliente(Persona):
    def __init__(self, name, lastname, numero_cuenta, balance = 0):
        super().__init__(name, lastname)
        self.numero_cuenta = numero_cuenta
        self.balance = balance

    def __str__(self):
        return f'Buenas tardes {self.name} {self.lastname}\n tu cuenta {self.numero_cuenta} tiene un balance de ${self.balance}'

    def depositar(self, cantidad):
        self.balance += cantidad
        print(f"Se ha depositado {cantidad}")

    def retirar(self, cantidad):
            if self.balance >= cantidad:
                self.balance -= cantidad
                print("Retiro realizado.")
            else:
                print(f"Fondos insuficientes.")

def crear_cliente():
    nombre = input("Ingrese su name: ")
    apellido = input("Ingrese su lastname: ")
    numero_cuenta = randint(10 ** 15, 10 ** 16 - 1)
    cliente = Cliente(nombre, apellido, numero_cuenta)
    return cliente


def sesion():
    new_client = crear_cliente()
    print(new_client)
    opcion = 0
    while opcion != "S":
        print("Ingrese una de las opciones: \t'R': Retirar \t'D': Depositar \t'S': Salir")
        opcion = input()

        if opcion == 'D':
            monto = int(input("Ingrese la cantidad del monto a Depositar: \n"))
            new_client.depositar(monto)

        elif opcion == 'R':
            monto = int(input("Ingrese la cantidad del monto a retirar: \n"))
            new_client.retirar(monto)

        print(new_client)
    print("Gracias por usar esta app de banco")


sesion()

