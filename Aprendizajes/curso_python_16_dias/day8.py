"""
Generator class
"""

def vida():
    vida_restante = 3
    while vida_restante > 0:
        yield f"Te quedan {vida_restante} vidas"
        vida_restante -= 1
    yield "Game Over"

perder_vida = vida()

print(next(perder_vida))
print(next(perder_vida))
print(next(perder_vida))
print(next(perder_vida))

def suma():
    turno = 1
    while turno > 0:
        yield f"El número {turno}"
        turno += 1

prueba = suma()
print(next(prueba))
print(next(prueba))
print(next(prueba))
print(next(prueba))
print(next(prueba))