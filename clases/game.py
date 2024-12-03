# game.py
import pygame as pg
import sys
from clases.settings import *
from clases.mapa import Mapa
from clases.tower import *
from clases.sidebar import Sidebar
from clases.enemy import *
from clases.player import *
from clases.animation import *
from clases.base import *
from clases.startScreen import *
from clases.wave import *
from clases.waves import *
from clases.levels import *
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.display = pg.Surface(DISPLAY_SIZE)
        self.wave_timer = 0 
        # Fuentes
        self.font_title = pg.font.Font("font/ARCADECLASSIC.ttf", 72)
        self.font_option = pg.font.Font("font/ARCADECLASSIC.ttf", 48)
        self.font = pg.font.Font(None, 12)

        # Pantalla de inicio
        self.start_screen = StartScreen(
            screen=self.screen,
            font_title=self.font_title,
            font_option=self.font_option,
            background_path="assets/fondos/fondoInicio2.jpg"
        )

        # Nivel actual y datos iniciales
        self.current_level = 1
        self.towers = []
        self.projectiles = []
        self.load_level(self.current_level)

        # Jugador, base y recursos
        self.player = Player(level=self.current_level)

        self.base = Base(
            position=self.mapa.base_position,
            image_paths=[
                "assets/simbolo/vicuna1.png",
                "assets/simbolo/vicuna2.png",
                "assets/simbolo/vicuna3.png",
                "assets/simbolo/vicuna4.png",
                "assets/simbolo/vicuna5.png"
            ],
            health=100
        )
        self.coin_animation = Animation(
            image_paths=[
                "assets/coins/coin1.png",
                "assets/coins/coin2.png",
                "assets/coins/coin3.png",
                "assets/coins/coin4.png"
            ],
            position=(10, RES[1] - 50),
            frame_duration=100,
            loop=True,
            size=(32, 32)
        )
        

        # Barra lateral (torres)
        self.sidebar = Sidebar(
            180,
            70,
            [
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (10, 15)),
                    'name': 'Tower A',
                    'cost': 10,
                    'range': 50,
                    'damage': 1,
                    'speed': 0.5
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (10, 15)),
                    'name': 'Tower B',
                    'cost': 20,
                    'range': 60,
                    'damage': 1.5,
                    'speed': 0.5
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (10, 15)),
                    'name': 'Tower C',
                    'cost': 30,
                    'range': 220,
                    'damage': 0.5,
                    'speed': 0.3
                }
            ],
            self.font
        )

    def load_level(self, level):
        """
        Carga el mapa y configura las oleadas de enemigos para el nivel.
        """
        self.mapa = Mapa(f"maps/map{level}.txt")
        self.enemy_group = []  # Lista de enemigos activos
        self.projectiles = []  # Lista de proyectiles activos

        # Obtener la configuración del nivel
        level_config = ENEMIES_BY_LEVEL.get(level)
        if not level_config:
            raise ValueError(f"No se encontró la configuración para el nivel {level}")

        path = self.mapa.path  # Camino del mapa

        # Crear oleadas según la configuración del nivel
        self.waves = []
        for _ in range(level_config["waves"]):  # Número de oleadas
            enemies = []
            for enemy_config in level_config["enemies"]:
                for _ in range(enemy_config["count"]):  # Cantidad de enemigos
                    enemies.append(
                        AnimatedEnemy(
                            grid_path=path,
                            animation_frames_by_direction=enemy_config["frames_by_direction"],
                            reward=enemy_config["reward"],
                            health=enemy_config["health"],
                            speed=enemy_config["speed"],
                            damage=enemy_config["damage"],
                        )
                    )
            # Crear la oleada con los enemigos y la frecuencia de spawn
            self.waves.append(Wave(enemies, spawn_rate=2.0))  # Cambia el spawn_rate si es necesario

        self.current_wave_index = 0  # Reiniciar al inicio de las oleadas
        self.wave_timer = 0  # Temporizador entre oleadas

    def update(self):
        """
        Actualiza el estado del juego.
        """
        dt = self.clock.tick(FPS) / 1000.0
        self.coin_animation.update()
        self.base.animation.update()
        self.mapa.vicuna_animation.update()

        # Actualizar oleadas
        if self.current_wave_index < len(self.waves):
            current_wave = self.waves[self.current_wave_index]
            if current_wave.is_finished():  # Si la oleada actual terminó
                self.wave_timer += dt
                if self.wave_timer >= 3.0:  # Tiempo entre oleadas (ajústalo según sea necesario)
                    self.current_wave_index += 1
                    self.wave_timer = 0
            else:
                current_wave.update(dt, self.enemy_group)

        # Actualizar enemigos
        for enemy in self.enemy_group[:]:
            enemy.move(dt)
            if enemy.path_index >= len(enemy.grid_path):  # Si llegó al final del camino
                self.base.take_damage(enemy.damage)
                self.enemy_group.remove(enemy)
            elif enemy.is_dead:
                self.enemy_group.remove(enemy)
                self.player.add_resources(enemy.reward)

        # Actualizar proyectiles
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if projectile.is_finished():
                self.projectiles.remove(projectile)

        # Actualizar torres
        for tower in self.towers:
            tower.attack(self.enemy_group, self.projectiles, self.player)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        """
        Maneja clics en la pantalla.
        """
        if self.sidebar.rect.collidepoint(pos):
            self.sidebar.handle_click(pos)
        else:
            if self.sidebar.selected_tower is not None:
                tile_coords = self.mapa.detect_tile(pos, RES, DISPLAY_SIZE)
                if tile_coords:
                    grid_x, grid_y = tile_coords
                    if not any(tower.position == (grid_x, grid_y) for tower in self.towers):
                        selected_tower = self.sidebar.towers[self.sidebar.selected_tower]
                        tower_cost = selected_tower['cost']
                        if self.player.spend_resources(tower_cost):
                            self.towers.append(
                                Tower(
                                    (grid_x, grid_y),
                                    selected_tower['image_small'],
                                    range=selected_tower['range'],
                                    damage=selected_tower['damage'],
                                    attack_speed=selected_tower['speed']
                                )
                            )
                            self.sidebar.selected_tower = None

    def draw(self):
        """
        Dibuja el estado del juego en la pantalla.
        """
        self.display.fill((0, 0, 0))
        self.mapa.draw(self.display)
        for tower in self.towers:
            tower.draw(self.display)
        self.base.draw(self.display)
        for enemy in self.enemy_group:
            enemy.draw(self.display)
        for projectile in self.projectiles:
            projectile.draw(self.display)
        

        self.screen.blit(pg.transform.scale(self.display, RES), (0, 0))
        self.sidebar.draw(self.screen)
        self.base.draw(self.screen)
        self.coin_animation.draw(self.screen)

        resources_text = self.font.render(f"{self.player.resources}", True, (255, 255, 255))
        self.screen.blit(resources_text, (50, RES[1] - 40))
        pg.display.flip()

    def show_start_screen(self):
        """
        Muestra la pantalla de inicio.
        """
        while True:
            if self.start_screen.handle_events():
                break
            self.start_screen.draw()
            self.clock.tick(FPS)

    def run(self):
        """
        Ejecuta el juego.
        """
        self.show_start_screen()
        while True:
            self.check_events()
            self.update()
            self.draw()
