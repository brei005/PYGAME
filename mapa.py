# mapa.py
import pygame as pg
from settings import *

class Mapa:
    def __init__(self, filename):
        self.map_data = self.load_map(filename)
        self.textures = self.load_textures()
        self.font = pg.font.Font(None, 11)  # Tamaño ajustado para mejor visibilidad

    def load_map(self, filename):
        """Carga el mapa desde un archivo de texto."""
        with open(filename) as f:
            return [[int(c) for c in row] for row in f.read().split('\n')]

    def load_textures(self):
        """Carga las texturas según los tipos de terreno definidos."""
        textures = {}
        for terrain_type, texture_path in TERRAIN_TYPES.items():
            image = pg.image.load(texture_path).convert()
            image.set_colorkey((0, 0, 0))
            textures[terrain_type] = image
        return textures

    def draw_text(self, text, x, y, color=(255, 255, 255), display=None):
        """Dibuja texto en la pantalla."""
        text_surface = self.font.render(text, True, color)
        display.blit(text_surface, (x, y))

    def draw(self, display):
        """Dibuja el mapa en la pantalla con un gap entre los bloques."""
        
        for y, row in enumerate(self.map_data):  # Iterar filas (y)
            for x, tile in enumerate(row):  # Iterar columnas (x)
                if tile in self.textures:
                    # Coordenadas del bloque en pantalla con gap aplicado
                    block_x = 130 + x * (10 + GAP_x) - y * (10 + GAP_x)
                    block_y = 80 + x * (5 + GAP_y) + y * (5 + GAP_y)
                    display.blit(self.textures[tile], (block_x, block_y))
                    # Coordenadas del texto
                    #self.draw_text(f"{x},{y}", block_x + 5, block_y + 5, display=display)


    def is_valid_tile(self, x, y):
        """Verifica si el tile en (x, y) es válido para colocar una torre."""
        return 0 <= x < len(self.map_data[0]) and 0 <= y < len(self.map_data) and self.map_data[y][x] == 0

    def place_tower(self, x, y):
        """Coloca una torre en el tile si es válido."""
        if self.is_valid_tile(x, y):
            self.map_data[y][x] = 1  # Marca el tile como ocupado por una torre
            return True
        return False
    def detect_tile(self, click_pos, window_size, display_size):
        """Detecta el tile en el que ocurrió el clic, ajustando por la escala y el gap."""
        click_x, click_y = click_pos

        # Ajustar las coordenadas del clic a la escala de la superficie interna
        scale_x = display_size[0] / window_size[0]
        scale_y = display_size[1] / window_size[1]
        adjusted_x = click_x * scale_x
        adjusted_y = click_y * scale_y

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                # Coordenadas del bloque con gap aplicado
                block_x = 130 + x * (10 + GAP_x) - y * (10 + GAP_x)
                block_y = 80 + x * (5 + GAP_y) + y * (5 +GAP_y)

                # Coordenadas de los vértices del bloque (isométrico)
                top = (block_x, block_y)
                bottom = (block_x, block_y + 10 + GAP_y)
                left = (block_x - (10 + GAP_x), block_y + (5 + GAP_y))
                right = (block_x + (10 + GAP_x), block_y + (5 + GAP_y))

                # Verificar si el clic ajustado está dentro del rombo
                if self.is_point_in_diamond(adjusted_x, adjusted_y, top, bottom, left, right):
                    return x, y  # Coordenadas del bloque en la cuadrícula

        return None  # Ningún bloque detectado


    def is_point_in_diamond(self, px, py, top, bottom, left, right):
        """
        Verifica si un punto está dentro de un rombo definido por cuatro vértices.
        Divide el rombo en dos triángulos para realizar la verificación.
        """
        return (
            self.is_point_in_triangle(px, py, top, left, right) or
            self.is_point_in_triangle(px, py, bottom, left, right)
        )
    def is_point_in_triangle(self, px, py, v1, v2, v3):
        """
        Verifica si un punto está dentro de un triángulo definido por tres vértices.
        Usa el signo del área para determinar si el punto está dentro del triángulo.
        """
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign((px, py), v1, v2) < 0.0
        b2 = sign((px, py), v2, v3) < 0.0
        b3 = sign((px, py), v3, v1) < 0.0

        return b1 == b2 == b3



    


