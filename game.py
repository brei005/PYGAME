# game.py
import pygame as pg
import sys
from settings import *
from mapa import Mapa
from tower import *
from sidebar import Sidebar

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.display = pg.Surface(DISPLAY_SIZE)
        self.font = pg.font.Font(None, 12)
        self.towers = []  # Lista para almacenar torres
        self.selected_tower = None 
        self.sidebar = Sidebar(
            180, 
            70, 
            [
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (50, 50)),  # Tamaño para la barra
                    'image_small': pg.transform.scale(pg.image.load("towers/towerA.png").convert_alpha(), (10, 15)),  # Tamaño para el mapa
                    'name': 'Tower A',
                    'cost': 10
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerB.png").convert_alpha(), (10, 15)),
                    'name': 'Tower B',
                    'cost': 20
                },
                {
                    'image_large': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (50, 50)),
                    'image_small': pg.transform.scale(pg.image.load("towers/towerC.png").convert_alpha(), (10, 15)),
                    'name': 'Tower C',
                    'cost': 30
                }
            ],
            self.font
        )

        # Nivel actual
        self.current_level = 1
        self.load_level(self.current_level)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """Dibuja texto en la pantalla."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, (x, y))

    def load_level(self, level):
        filename = f'maps/map{level}.txt'
        self.mapa = Mapa(filename)

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

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
                        self.towers.append(Tower((grid_x, grid_y), selected_tower['image_small']))  # Usa la imagen pequeña
                        print(f"{selected_tower['name']} colocada en ({grid_x}, {grid_y})")
                        self.sidebar.selected_tower = None


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
        # Dibuja el mapa y el contenido en la superficie intermedia
        self.display.fill((0, 0, 0))  # Fondo negro en la superficie interna
        self.mapa.draw(self.display)  # Dibuja el mapa en la superficie interna

        for tower in self.towers:
            tower.draw(self.display)

        # Escalar la superficie interna y dibujarla en la pantalla principal
        self.screen.blit(pg.transform.scale(self.display, RES), (0, 0))

        # Dibujar la barra lateral
        self.sidebar.draw(self.screen)

        pg.display.flip()  # Actualiza la pantalla

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()