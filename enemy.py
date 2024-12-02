import pygame as pg
from settings import *

class Enemy:
    def __init__(self, grid_position, texture_path, reward=10, health=100, path=None, speed=0.05):

        """
        Inicializa al enemigo con una posición en la grilla, textura y salud.
        """
        self.grid_position = grid_position  # Posición en la grilla (x, y)
        self.health = health  # Salud del enemigo
        self.max_health = health  # Salud máxima para calcular la barra
        self.image = pg.image.load(texture_path).convert_alpha()  # Cargar textura
        self.image = pg.transform.scale(self.image, (15, 20))  # Escalar textura para adaptarla al bloque
        self.reward = reward
        
        self.path = path or []  # Lista de posiciones que el enemigo recorrerá
        self.position_index = 0  # Indice de la posición actual en el camino
        self.progress = 0  # Progreso del movimiento entre posiciones
        self.speed = speed  # Velocidad de movimiento del enemigo

    def get_screen_position(self):
        """
        Convierte la posición en la grilla a coordenadas de pantalla.
        """
        grid_x, grid_y = self.grid_position
        screen_x = 130 + grid_x * (10 + GAP_x) - grid_y * (10 + GAP_x)
        screen_y = 80 + grid_x * (5 + GAP_y) + grid_y * (5 + GAP_y)
        return screen_x, screen_y
    def update(self):
            """
            Actualiza la posición del enemigo.
            """
            if self.position_index < len(self.path) - 1:
                current_x, current_y = self.path[self.position_index]
                next_x, next_y = self.path[self.position_index + 1]

                direction_x = next_x - current_x
                direction_y = next_y - current_y

                distance = (direction_x**2 + direction_y**2)**0.5
                if distance > 0:  # Evitar división por cero
                    direction_x /= distance
                    direction_y /= distance

                self.progress += self.speed
                self.x = current_x + self.progress * direction_x
                self.y = current_y + self.progress * direction_y

                if self.progress >= distance:
                    self.position_index += 1
                    self.progress = 0
    def draw(self, display):
        """
        Dibuja al enemigo y su barra de vida en la pantalla.
        """
        screen_x, screen_y = self.get_screen_position()

        # Dibujar el enemigo
        display.blit(self.image, (screen_x, screen_y - 15))  # Ajustar para que quede sobre el bloque

        # Dibujar la barra de vida justo encima de la textura
        health_bar_width = 20
        health_bar_height = 4
        health_x = screen_x + (15 // 2) - (health_bar_width // 2)  # Centrar la barra en la cabeza
        health_y = screen_y - 20  # Justo encima del enemigo
        health_percentage = max(0, self.health / self.max_health)  # Evitar valores negativos
        pg.draw.rect(display, (0, 0, 0), (health_x, health_y, health_bar_width, health_bar_height))  # Fondo negro
        pg.draw.rect(display, (0, 255, 0), (health_x, health_y, health_bar_width * health_percentage, health_bar_height))  # Barra verde

    def take_damage(self, amount):
        """
        Reduce la salud del enemigo por el daño recibido.
        """
        self.health -= amount
        print(f"Enemigo en {self.grid_position} recibió {amount} de daño. Salud restante: {self.health}")
        if self.health <= 0:
            print("El enemigo ha sido eliminado")
