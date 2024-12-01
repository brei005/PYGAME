# game.py
import pygame as pg
import sys
from settings import *
from mapa import Mapa
from tower import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.display = pg.Surface(DISPLAY_SIZE)
        self.font = pg.font.Font(None, 10)
        self.towers = []  # Lista para almacenar torres
        self.tower_image = pg.image.load("towers/towerB.png").convert_alpha()  # Carga de la imagen
        self.tower_image = pg.transform.scale(self.tower_image, (10, 15))  # Ajustar dimensiones aquí

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
        """Maneja el clic del ratón para colocar torres."""
        tile_coords = self.mapa.detect_tile(pos, RES, DISPLAY_SIZE)

        if tile_coords:
            grid_x, grid_y = tile_coords

            # Verificar si ya hay una torre en esa posición
            if not any(tower.position == (grid_x, grid_y) for tower in self.towers):
                # Colocar una nueva torre
                self.towers.append(Tower((grid_x, grid_y), self.tower_image))
                print(f"Torre colocada en ({grid_x}, {grid_y})")
            else:
                print("Ya hay una torre en este bloque")
        else:
            print("Clic fuera de cualquier bloque")

    def draw(self):
        self.display.fill((0, 0, 0))
        self.mapa.draw(self.display)

        for tower in self.towers:
            tower.draw(self.display)
        # Dibujar las torres (donde el mapa tiene un `2`)
        for y, row in enumerate(self.mapa.map_data):
            for x, tile in enumerate(row):
                if tile == 2:
                    pg.draw.rect(self.display, (255, 0, 0), (x * 10, y * 10, 10, 10))

        self.screen.blit(pg.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()