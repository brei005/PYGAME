import pygame as pg
import math

class Projectile:
    def __init__(self, start_pos, target_pos, speed=50):
        """
        Inicializa un proyectil.
        - `start_pos`: Posición inicial del proyectil (en pantalla).
        - `target_pos`: Posición del objetivo (en pantalla).
        - `speed`: Velocidad del proyectil.
        """
        self.x, self.y = start_pos  # Posición actual del proyectil
        self.target_x, self.target_y = target_pos  # Posición del objetivo
        self.target_x =target_pos[0]+5
        self.target_y=target_pos[1]-7
        self.speed = speed  # Velocidad del proyectil
        self.time = 0  # Tiempo transcurrido
        self.finished = False  # Si el proyectil ha alcanzado el objetivo

        # Cálculo de la distancia y el ángulo inicial
        self.distance = math.dist(start_pos, target_pos)
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

        # Altura máxima de la parábola (curvatura del disparo)
        self.height = 10  # Ajustar según lo desees

    def update(self, dt):
        """
        Actualiza la posición del proyectil considerando la perspectiva isométrica.
        - `dt`: Tiempo transcurrido desde la última actualización.
        """
        if self.finished:
            return  # No actualices si el proyectil ya alcanzó el objetivo

        # Movimiento horizontal (progreso hacia el objetivo)
        progress = (self.time * self.speed) / self.distance
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

        # Movimiento vertical con una parábola para simular caída
        self.y -= 4 * self.height * progress * (1 - progress)  # Altura parabólica

        # Verificar si alcanzó el objetivo
        if math.dist((self.x, self.y), (self.target_x, self.target_y)) <= 5:  # Tolerancia de impacto
            self.finished = True  # Marcar el proyectil como finalizado

    def is_finished(self):
        """
        Verifica si el proyectil alcanzó su objetivo.
        """
        return self.finished

    def draw(self, display):
        """
        Dibuja el proyectil en la pantalla.
        """
        if not self.finished:
            pg.draw.circle(display, (255, 255, 0), (int(self.x), int(self.y)), 1)  # Proyectil amarillo