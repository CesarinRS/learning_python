"""
This script is available for practices
"""


class Libro():
    def __init__(self, titulo, autor, cantidad_paginas):
        self.titulo = titulo
        self.autor = autor
        self.cantidad_paginas = cantidad_paginas

    def __str__(self):
        return f'"{self.titulo}", de {self.autor}'

atomic_habits = Libro('Hábitos atomicos', 'James Clear', '235')

print(f'El libro que acabo de comprar es: {atomic_habits}')