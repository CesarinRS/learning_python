"""
Proyecto del día 7
"""
from random import randint


class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

class Cliente(Persona):
    def __init__(self, nombre, apellido, numero_cuenta, balance):
        super().__init__(nombre, apellido)
        self.numero_cuenta = numero_cuenta
        self.balance = balance

    def __str__(self):
        return f'Buenas tardes {self.nombre} {self.apellido}'

    def depositar(self, cantidad):
            if cantidad > 0:
                self.balance += cantidad
                return f"Su balance es de {self.balance}"
            else:
                return f'No es valido ${cantidad}'

    def retirar(self, cantidad):
            if cantidad > self.balance:
                return f"Fondos insuficientes. balance actual: ${self.balance}"
            else:
                self.balance -= cantidad
                return f'Su balance es de {self.balance}'

    def sesion(self):
        while True:
            peticion_usuario = input("Ingrese una de las opciones: \t1: Retirar \t2: Depositar \t3: Salir")

            if peticion_usuario == '1':
                print(f"Estimado {self.nombre}, a seleccionado la opción de retirar\n")
                monto = int(input("Ingrese la cantidad del monto a retirar: \n"))
                print(self.retirar(monto))
                continue

            elif peticion_usuario == '2':
                print(f"Estimado {self.nombre}, a seleccionado la opción de depositar\n")
                monto = int(input("Ingrese la cantidad del monto a depositar: \n"))
                print(self.depositar(monto))
                continue

            elif peticion_usuario == '3':
                print(f"Estimado {self.nombre}, gracias por usar nuestra app, ¡nos vemos pronto!")
                break

            else:
                print("Opción invalida, vuelve a intentarlo")
                continue

print("=== Registro del cliente ===")
nombre = input("Ingrese su nombre: ")
apellido = input("Ingrese su apellido: ")
numero_cuenta = randint(10**15, 10**16 - 1)

while True:
    try:
        balance_inicial = float(input("Balance inicial: $"))
        break
    except ValueError:
        print("Por favor, ingresa un número válido.")

cliente  = Cliente(nombre, apellido, numero_cuenta, balance_inicial)

print(cliente)
cliente.sesion()