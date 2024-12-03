# mapa.py
import pygame as pg
from clases.settings import *
from clases.animation import *

class Mapa:
    def __init__(self, filename):
        self.map_data = self.load_map(filename)
        self.textures = self.load_textures()
        self.font = pg.font.Font(None, 11)
        
        # Animación de la vicuña en el mapa
        self.vicuna_animation = Animation(
            image_paths=[
                "assets/coins/coin1.png",
                "assets/coins/coin2.png",
                "assets/coins/coin3.png",
                "assets/coins/coin4.png"
            ],
            position=(0, 0),  # La posición será dinámica según la base
            frame_duration=150,
            loop=True,size = (10,15)
        )
        self.base_position = self.find_base()  # Encuentra la posición de la base
        
        self.start_position = self.find_start()
        self.path = self.generate_path() 
    def find_start(self):
        """Encuentra el punto de inicio (marcado con 'x') en el mapa."""
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 'x':
                    return (x, y)  # Coordenadas del inicio como tupla
        raise ValueError("El mapa no contiene un punto de inicio ('x').")

    def generate_path(self):
        """
        Genera el camino desde el punto de inicio ('x') hasta el punto final ('2').
        """
        path = []
        start = None
        end = None

        # Buscar el punto de inicio ('x') y el final ('2') en el mapa
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 'x':
                    start = (x, y)
                elif tile == '2':
                    end = (x, y)
                elif tile == '1':
                    path.append((x, y))  # Agregar los tiles del camino
        
        
        if not start or not end:
            raise ValueError("El mapa debe contener un punto de inicio ('x') y un punto final ('2').")

        # Ordenar los tiles del camino para que formen una trayectoria desde 'x' hasta '2'
        sorted_path = [start]
        while path:
            # Encontrar el tile más cercano al último en el camino
            last_tile = sorted_path[-1]
            next_tile = min(path, key=lambda tile: abs(tile[0] - last_tile[0]) + abs(tile[1] - last_tile[1]))
            sorted_path.append(next_tile)
            path.remove(next_tile)
        #print(sorted_path)
        # Agregar el punto final al camino
        sorted_path.append(end)
        return sorted_path

    def find_base(self):
        """Encuentra la posición de la base (representada por el valor 2 en el mapa)."""
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == '2':  # 2 representa la base
                    return (x, y)
        return None  # Si no se encuentra la base
    def load_map(self, filename):
        """
        Carga el mapa desde un archivo de texto.
        Permite caracteres como 'x', '1', '2', etc.
        """
        with open(filename) as f:
            return [list(row) for row in f.read().strip().split('\n')]


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
                    block_x = INICIO_X + x * (10 + GAP_x) - y * (10 + GAP_x)
                    block_y = INICIO_Y + x * (5 + GAP_y) + y * (5 + GAP_y)
                    display.blit(self.textures[tile], (block_x, block_y))
                    # Coordenadas del texto
                    #self.draw_text(f"{x},{y}", block_x + 5, block_y + 5, display=display)
                # Si es la posición de la base, dibujar la vicuña estática
                # Si es la posición de la base, dibujar la animación de la vicuña
                if (x, y) == self.base_position:
                    self.draw_vicuna(display, block_x, block_y)
    def draw_vicuna(self, display, block_x, block_y):
        """Dibuja la animación de la vicuña en la posición de la base."""
        self.vicuna_animation.position = (block_x+5, block_y - 7)  # Ajustar posición
        self.vicuna_animation.draw(display)

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
                block_x = INICIO_X + x * (10 + GAP_x) - y * (10 + GAP_x)
                block_y = INICIO_Y + x * (5 + GAP_y) + y * (5 +GAP_y)

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