from enemy import Enemy


class Dog(Enemy):
    """Perro enemigo que usa el movimiento compartido de Enemy."""

    image_file = "dog.png"
    size = (54, 64)
    speed = 112.5
