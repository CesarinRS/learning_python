"""Tipo de enemigo gato."""

from enemy import Enemy


class Cat(Enemy):
    """Gato enemigo, más rápido que el perro."""

    image_file = "cat.png"
    size = (40, 48)
    speed = 180
