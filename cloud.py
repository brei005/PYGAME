import pygame as pg
import random
from settings import RES

class Cloud:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed

    def move(self):
        """Mueve la nube a la izquierda"""
        self.x -= self.speed
        # Si la nube sale de la pantalla por la izquierda, la colocamos al final.
        if self.x < -self.image.get_width():
            self.x = RES[0]

    def draw(self, screen):
        """Dibuja la nube en la pantalla"""
        screen.blit(self.image, (self.x, self.y))

    @classmethod
    def create_random_cloud(cls):
        """Crea una nube en una posición aleatoria"""
        x = random.randint(RES[0], RES[0] + 1000)  # Posición fuera de la pantalla
        y = random.randint(50, 200)  # Altura aleatoria de la nube
        image = pg.image.load("assets/cloud.png").convert_alpha()
        speed = random.uniform(0.1, 0.5)  # Velocidad aleatoria de la nube
        return cls(x, y, image, speed)
