# enemy.py
import pygame as pg
import math
from clases.settings import *
import pygame as pg
import math
from clases.animation import Animation

class AnimatedEnemy:
    def __init__(self, grid_path, animation_frames_by_direction, reward=10, health=100, speed=10, damage=10):
        """
        Inicializa un enemigo animado con diferentes animaciones según la dirección.
        - `animation_frames_by_direction`: Diccionario con animaciones para cada dirección ('up', 'down', 'left', 'right').
        """
        self.grid_path = grid_path
        self.animations = {
            "up": Animation(animation_frames_by_direction["up"], position=(0, 0), frame_duration=170, loop=True, size=(20, 25)),
            "down": Animation(animation_frames_by_direction["down"], position=(0, 0), frame_duration=170, loop=True, size=(20, 25)),
            "left": Animation(animation_frames_by_direction["left"], position=(0, 0), frame_duration=170, loop=True, size=(20, 25)),
            "right": Animation(animation_frames_by_direction["right"], position=(0, 0), frame_duration=170, loop=True, size=(20, 25))
        }
        self.current_animation = self.animations["up"]  # Animación inicial
        self.reward = reward
        self.health = health
        self.max_health = health
        self.speed = speed
        self.damage = damage
        self.grid_position = grid_path[0]
        self.path_index = 0
        self.position = self.get_screen_position()
        self.is_dead = False

    def get_screen_position(self):
        """Convierte la posición en la grilla a coordenadas de pantalla."""
        grid_x, grid_y = self.grid_position
        screen_x = INICIO_X + grid_x * (10 + GAP_x) - grid_y * (10 + GAP_x)
        screen_y = INICIO_Y + grid_x * (5 + GAP_y) + grid_y * (5 + GAP_y)
        return screen_x, screen_y

    def move(self, dt):
        """Mueve al enemigo a lo largo del camino y actualiza la animación según la dirección."""
        if self.path_index >= len(self.grid_path) or self.is_dead:
            return

        # Obtener la posición actual y la siguiente en la grilla
        current_grid_pos = self.grid_path[self.path_index]
        next_grid_pos = self.grid_path[self.path_index + 1] if self.path_index + 1 < len(self.grid_path) else None

        # Calcular dirección en la grilla
        if next_grid_pos:
            direction_vector = (next_grid_pos[0] - current_grid_pos[0], next_grid_pos[1] - current_grid_pos[1])

            # Cambiar la animación según la dirección en la grilla
            if direction_vector[0] > 0:  # Movimiento hacia la derecha
                self.current_animation = self.animations["right"]
            elif direction_vector[0] < 0:  # Movimiento hacia la izquierda
                self.current_animation = self.animations["left"]
            elif direction_vector[1] > 0:  # Movimiento hacia abajo
                self.current_animation = self.animations["down"]
            elif direction_vector[1] < 0:  # Movimiento hacia arriba
                self.current_animation = self.animations["up"]

        # Actualizar posición en pantalla
        current_tile_screen = self.get_screen_position()
        next_tile_screen = self.get_next_tile()

        direction_vector_screen = (
            next_tile_screen[0] - current_tile_screen[0],
            next_tile_screen[1] - current_tile_screen[1],
        )
        distance_screen = math.sqrt(direction_vector_screen[0]**2 + direction_vector_screen[1]**2)

        if distance_screen > 0:
            normalized_direction = (
                direction_vector_screen[0] / distance_screen,
                direction_vector_screen[1] / distance_screen,
            )
            self.position = (
                self.position[0] + normalized_direction[0] * self.speed * dt,
                self.position[1] + normalized_direction[1] * self.speed * dt,
            )

        # Actualizar animación
        self.current_animation.update()

        # Verificar si llegó al siguiente tile en pantalla
        new_distance_screen = math.sqrt(
            (next_tile_screen[0] - self.position[0])**2 + (next_tile_screen[1] - self.position[1])**2
        )
        if new_distance_screen < 2:  # Ajusta la tolerancia según sea necesario
            self.path_index += 1
            if self.path_index < len(self.grid_path):
                self.grid_position = self.grid_path[self.path_index]
            else:
                # Si llega al final del camino, hace daño a la base y "muere"
                self.on_reach_base()


    def get_next_tile(self):
        """Obtiene el próximo tile en el camino."""
        if self.path_index + 1 < len(self.grid_path):
            grid_x, grid_y = self.grid_path[self.path_index + 1]
            screen_x = INICIO_X + grid_x * (10 + GAP_x) - grid_y * (10 + GAP_x)
            screen_y = INICIO_Y + grid_x * (5 + GAP_y) + grid_y * (5 + GAP_y)
            return screen_x, screen_y
        return self.get_screen_position()

    def draw(self, display):
        """Dibuja al enemigo con su animación y barra de vida."""
        self.current_animation.position = (self.position[0] + 3, self.position[1] - 18)
        self.current_animation.draw(display)
        self.draw_health_bar(display)

    def draw_health_bar(self, display):
        """Dibuja la barra de vida sobre el enemigo."""
        screen_x, screen_y = self.position
        health_bar_width = 20
        health_bar_height = 4
        health_x = screen_x + (15 // 2) - (health_bar_width // 2)
        health_y = screen_y - 20
        health_percentage = max(0, self.health / self.max_health)
        pg.draw.rect(display, (0, 0, 0), (health_x, health_y, health_bar_width, health_bar_height))
        pg.draw.rect(display, (0, 255, 0), (health_x, health_y, health_bar_width * health_percentage, health_bar_height))

    def on_reach_base(self):
        """Acción cuando el enemigo llega a la base."""
        print(f"El enemigo llegó a la base e infligió {self.damage} de daño.")
        self.is_dead = True  # El enemigo se marca como eliminado
    def take_damage(self, damage, player=None):
        """
        Reduce la salud del enemigo por el daño recibido.
        - `damage`: Cantidad de daño infligido.
        - `player`: Referencia al jugador, para añadir recompensas si el enemigo muere.
        """
        self.health -= damage  # Reducir la salud del enemigo
        print(f"Enemigo recibió {damage} de daño. Salud restante: {self.health}")
        
        if self.health <= 0:
            self.health = 0
            self.is_dead = True  # Marcar al enemigo como muerto
            print("Enemigo eliminado.")
            
            # Dar recompensa al jugador si se especifica
            if player:
                player.add_resources(self.reward)