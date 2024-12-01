from settings import *
import pygame as pg

class Tower:
    def __init__(self, position, image):
        self.position = position  # Posición en la cuadrícula (x, y)
        self.image = image  # Imagen de la torre
        self.range = 50  # Rango de ataque
        self.damage = 10  # Daño por disparo
    
    def draw(self, display):
        """Dibuja la torre en la pantalla."""
        block_x = 130 + self.position[0] * (10 + GAP_x) - self.position[1] * (10 + GAP_x)
        block_y = 80 + self.position[0] * (5 + GAP_y) + self.position[1] * (5 + GAP_y)
        display.blit(self.image, (block_x + 4, block_y - 8))  # Ajustar la torre para que quede encima

