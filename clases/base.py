import pygame as pg
from clases.animation import Animation
from clases.settings import *

class Base:
    def __init__(self, position, image_paths, health=100):
        """
        Clase que representa la base del jugador.
        - `position`: Posición de la base en el mapa (coordenadas de la cuadrícula).
        - `image_paths`: Lista de imágenes para la animación.
        - `health`: Salud inicial de la base.
        """
        self.position = position
        self.health = health
        self.max_health = health  # Salud máxima para calcular la barra de vida
        self.animation = Animation(
            image_paths=image_paths,
            position=(RES[0] - 145, 5),  # Esquina superior derecha
            frame_duration=150,
            loop=True,
            size= (140,140)
        )
    def take_damage(self, amount):
        """Reduce la salud de la base."""
        self.health -= amount
        if self.health < 0:
            self.health = 0  # Evitar salud negativa
        print(f"La base recibió {amount} de daño. Salud restante: {self.health}")

    def draw(self, screen):
        """Dibuja la base y su barra de vida en la pantalla."""
        # Dibuja la animación de la vicuña
        self.animation.draw(screen)
        
        # Dibuja la barra de vida
        bar_width = 135  # Ancho total de la barra
        BAR_X, BAR_Y = (RES[0] - 142,147)
        health_width = int((self.health / self.max_health) * bar_width)
        pg.draw.rect(screen, (255, 0, 0), (BAR_X, BAR_Y, bar_width, 10))  # Fondo rojo
        pg.draw.rect(screen, (0, 255, 0), (BAR_X, BAR_Y, health_width, 10))  # Salud restante
