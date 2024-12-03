from clases.settings import *
import pygame as pg
import math
from clases.enemy import *
import time
from clases.projectile import *
class Tower:
    def __init__(self, position, image, range=50, damage=10, attack_speed=1.0):
        """
        Inicializa la torre.
        - `attack_speed` es la cadencia, el tiempo en segundos entre disparos.
        """
        self.position = position  # Posición en la cuadrícula (x, y)
        self.image = image  # Imagen de la torre
        self.range = range  # Rango de ataque
        self.damage = damage  # Daño por disparo
        self.attack_speed = attack_speed  # Tiempo entre disparos en segundos
        self.last_attack_time = 0  # Tiempo del último disparo
    
    def draw(self, display):
        """Dibuja la torre en la pantalla."""
        block_x = INICIO_X + self.position[0] * (10 + GAP_x) - self.position[1] * (10 + GAP_x)
        block_y = INICIO_Y + self.position[0] * (5 + GAP_y) + self.position[1] * (5 + GAP_y)
        display.blit(self.image, (block_x + 4, block_y - 8))  # Ajustar la torre para que quede encima
    def attack(self, enemies, projectiles,player):
        """
        Ataca al enemigo más cercano dentro del rango.
        - `enemies`: Lista de enemigos activos.
        - `projectiles`: Lista de proyectiles activos.
        """
        if self.is_on_cooldown():
            return  # No atacar si está en cooldown

        # Buscar el primer enemigo dentro del rango
        for enemy in enemies:
            if self.is_in_range(enemy):
                # Crear un proyectil hacia el enemigo
                projectile = Projectile(self.get_screen_position(), enemy.get_screen_position(), speed=150)
                projectiles.append(projectile)
                enemy.take_damage(self.damage,player)  # Infligir daño directamente
                self.start_cooldown()  # Iniciar el cooldown de la torre
                break
    def is_on_cooldown(self):
        """
        Verifica si la torre está en tiempo de recarga (cooldown).
        """
        current_time = time.time()  # Tiempo actual en segundos
        return current_time - self.last_attack_time < self.attack_speed

    def start_cooldown(self):
        """
        Inicia el cooldown al atacar.
        """
        self.last_attack_time = time.time()
    def is_in_range(self, enemy):
        """
        Verifica si un enemigo está dentro del rango de ataque.
        """
        tower_x, tower_y = self.get_screen_position()
        enemy_x, enemy_y = enemy.get_screen_position()
        distance = math.sqrt((tower_x - enemy_x) ** 2 + (tower_y - enemy_y) ** 2)
        return distance <= self.range

    def get_screen_position(self):
        """
        Obtiene la posición de la torre en la pantalla.
        """
        grid_x, grid_y = self.position
        screen_x = INICIO_X + grid_x * (10 + GAP_x) - grid_y * (10 + GAP_x)
        screen_y = INICIO_Y + grid_x * (5 + GAP_y) + grid_y * (5 + GAP_y)
        return screen_x, screen_y