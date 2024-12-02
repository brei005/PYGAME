# game.py
import pygame as pg
import sys
from settings import *
from mapa import Mapa
from tower import *
from sidebar import Sidebar
from enemy import *
from player import *
from animation import *
from base import *
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.display = pg.Surface(DISPLAY_SIZE)
        self.font = pg.font.Font(None, 12)
        # Nivel actual
        self.current_level = 1
        self.load_level(self.current_level)
        self.towers = []  # Lista para almacenar torres
        self.selected_tower = None 
        self.projectiles = []
        self.base = Base(
            position=self.mapa.base_position,
            image_paths=[
                "assets/simbolo/vicuna1.png",
                "assets/simbolo/vicuna2.png",
                "assets/simbolo/vicuna3.png",
                "assets/simbolo/vicuna4.png"
            ],
            health=100
        )
        # Inicializar animación de la moneda
        self.coin_animation = Animation(
            image_paths=[
                "assets/coins/coin1.png",
                "assets/coins/coin2.png",
                "assets/coins/coin3.png",
                "assets/coins/coin4.png"
            ],
            position=(10, RES[1] - 50),  # Posición en la esquina inferior izquierda
            frame_duration=100,  # Duración de cada frame en ms
            loop=True,
            size=(32, 32)  # Redimensionar cada imagen a 32x32 píxeles
        )
        self.player = Player(level=1)
        self.sidebar = Sidebar(
            180, 
            70, 
            [
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (50, 50)),  # Tamaño para la barra
                    'image_small': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (10, 15)),  # Tamaño para el mapa
                    'name': 'Tower A',
                    'cost': 10,
                    'range':50,
                    'damage':1,
                    'speed':0.5
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (10, 15)),
                    'name': 'Tower B',
                    'cost': 20,
                    'range':60,
                    'damage':1.5,
                    'speed':0.5
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (10, 15)),
                    'name': 'Tower C',
                    'cost': 30,
                    'range':220,
                    'damage':0.5,
                    'speed':0.3
                }
            ],
            self.font
        )
        self.enemy = Enemy((5, 5), "enemies/enemy1.png")
        

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """Dibuja texto en la pantalla."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, (x, y))

    def load_level(self, level):
        filename = f'maps/map{level}.txt'
        self.mapa = Mapa(filename)

    def update(self):
        """Actualiza el estado del juego."""
        self.coin_animation.update()  # Actualizar la animación de la moneda
        self.base.animation.update()
        self.mapa.vicuna_animation.update() 
        # Actualizar proyectiles
        for projectile in self.projectiles[:]:
            projectile.update(1 / FPS)  # Actualizar con tiempo basado en FPS
            if projectile.is_finished():
                self.projectiles.remove(projectile)  # Eliminar proyectil cuando finalice
                if self.enemy.health > 0:  # Asegurarse de que el enemigo esté vivo
                    for i in self.towers:
                        self.enemy.take_damage(i.damage)  # Infligir daño basado en el proyectil

        # Las torres atacan al enemigo
        for tower in self.towers:
            if self.enemy.health > 0:  # Solo si el enemigo está vivo
                tower.attack(self.enemy, self.projectiles)
        # Verificar si el enemigo alcanzó la base
        if self.enemy.health > 0 and self.enemy.grid_position == self.base.position:
            self.base.take_damage(10)  # Inflige daño a la base
            self.enemy.health = 0  # Elimina al enemigo
        # Verificar si el enemigo ha sido derrotado
        if self.enemy.health <= 0:
            self.player.add_resources(self.enemy.reward)  # Añade recursos al jugador
            print(f"Enemigo derrotado. Recursos ganados: {self.enemy.reward}")
            self.enemy.health = 0  # Evitar salud negativa
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
                self.handle_click(event.pos)

    def handle_click(self, pos):
        """Maneja los clics en la pantalla."""
        if self.sidebar.rect.collidepoint(pos):  # Si el clic está en la barra lateral
            self.sidebar.handle_click(pos)
        else:
            # Si hay una torre seleccionada, colócala en el mapa
            if self.sidebar.selected_tower is not None:
                tile_coords = self.mapa.detect_tile(pos, RES, DISPLAY_SIZE)
                if tile_coords:
                    grid_x, grid_y = tile_coords
                    if not any(tower.position == (grid_x, grid_y) for tower in self.towers):
                        selected_tower = self.sidebar.towers[self.sidebar.selected_tower]
                        tower_cost = selected_tower['cost']
                        
                        # Verificar si el jugador tiene suficientes recursos
                        if self.player.spend_resources(tower_cost):  # Gasta recursos
                            self.towers.append(
                                Tower(
                                    (grid_x, grid_y),
                                    selected_tower['image_small'],
                                    range=selected_tower['range'],
                                    damage=selected_tower['damage'],
                                    attack_speed=selected_tower['speed']
                                )
                            )
                            print(f"{selected_tower['name']} colocada en ({grid_x}, {grid_y}).")
                            self.sidebar.selected_tower = None  # Deseleccionar torre

    def handle_sidebar_click(self, pos):
        """Maneja los clics en la barra lateral."""
        # Rectángulo de la torre en la barra lateral
        tower_rect = pg.Rect(0, 0, 50, 40)
        if tower_rect.collidepoint(pos):
            # Alternar selección de la torre
            if self.selected_tower:
                print("Torre deseleccionada")
                self.selected_tower = None
            else:
                print("Torre seleccionada")
                self.selected_tower = self.tower_image


    def draw(self):
        """Dibuja el estado del juego en la pantalla."""
        self.display.fill((0, 0, 0))  # Limpiar la pantalla con fondo negro

        # Dibujar el mapa
        self.mapa.draw(self.display)

        # Dibujar torres
        for tower in self.towers:
            tower.draw(self.display)

        # Dibujar al enemigo
        if self.enemy.health > 0:  # Solo si el enemigo está vivo
            self.enemy.draw(self.display)

        # Dibujar proyectiles
        for projectile in self.projectiles:
            projectile.draw(self.display)
        

        # Dibujar la barra lateral
        self.screen.blit(pg.transform.scale(self.display, RES), (0, 0))
        self.sidebar.draw(self.screen)
        # Dibujar la base
        self.base.draw(self.screen)
        # Dibujar la animación de la moneda
        self.coin_animation.draw(self.screen)

        # Dibujar los recursos al lado de la moneda
        resources_bg_rect = pg.Rect(45, RES[1] - 50, 100, 40)  # Fondo detrás del texto
        pg.draw.rect(self.screen, (0, 0, 0), resources_bg_rect)  # Fondo negro
        resources_text = self.font.render(f"{self.player.resources}", True, (255, 255, 255))
        self.screen.blit(resources_text, (50, RES[1] - 40))  # Texto de recursos

        # Actualizar la pantalla
        pg.display.flip()


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()