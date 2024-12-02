from settings import *
import pygame as pg
import math
from enemy import *
import time
from projectile import *
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
        block_x = 130 + self.position[0] * (10 + GAP_x) - self.position[1] * (10 + GAP_x)
        block_y = 80 + self.position[0] * (5 + GAP_y) + self.position[1] * (5 + GAP_y)
        display.blit(self.image, (block_x + 4, block_y - 8))  # Ajustar la torre para que quede encima
    def attack(self, enemy, projectiles):
        """
        Ataca al enemigo si está dentro del rango y la torre está lista para disparar.
        """
        current_time = time.time()  # Obtiene el tiempo actual en segundos
        if current_time - self.last_attack_time >= self.attack_speed:
            # Verificar si el enemigo está dentro del rango
            tower_x = 130 + self.position[0] * (10 + GAP_x) - self.position[1] * (10 + GAP_x)
            tower_y = 80 + self.position[0] * (5 + GAP_y) + self.position[1] * (5 + GAP_y)
            enemy_x, enemy_y = enemy.get_screen_position()

            distance = math.sqrt((tower_x - enemy_x)**2 + (tower_y - enemy_y)**2)
            if distance <= self.range:
                print(f"Torre en {self.position} ataca al enemigo en {enemy.grid_position}")
                projectiles.append(Projectile((tower_x+7, tower_y-4), (enemy_x, enemy_y)))
                self.last_attack_time = current_time  # Registrar el tiempo del disparo

