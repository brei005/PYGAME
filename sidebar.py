import pygame as pg

class Sidebar:
    def __init__(self, width, height, towers, font):
        self.width = width  # Ancho de la barra lateral
        self.height = height  # Alto de la barra lateral
        self.rect = pg.Rect(0, 0, width, height)  # Rectángulo de la barra lateral
        self.towers = towers  # Lista de diccionarios con {'image': ..., 'name': ..., 'cost': ...}
        self.selected_tower = None  # Torre seleccionada
        self.font = font  # Fuente para texto
        self.tower_width = 60  # Ancho de cada ítem en la barra
        self.tower_height = 70  # Alto de cada ítem en la barra
        self.padding = 0  # Espacio entre ítems

    def handle_click(self, pos):
        """Maneja los clics dentro de la barra lateral."""
        for i, tower in enumerate(self.towers):
            # Calcular la posición de cada torre
            x = i * (self.tower_width + self.padding)
            y = 0
            tower_rect = pg.Rect(x, y, self.tower_width, self.tower_height)
            if tower_rect.collidepoint(pos):
                # Alternar selección de la torre
                if self.selected_tower == i:
                    print(f"Torre {i} ({tower['name']}) deseleccionada")
                    self.selected_tower = None
                else:
                    print(f"Torre {i} ({tower['name']}) seleccionada")
                    self.selected_tower = i

    def draw(self, screen):
        """Dibuja la barra lateral en la pantalla principal."""
        # Fondo de la barra lateral
        pg.draw.rect(screen, (80, 80, 80), self.rect)

        # Dibujar cada torre con su selección
        for i, tower in enumerate(self.towers):
            x = i * (self.tower_width + self.padding)+5
            y = 7
            screen.blit(tower['image_large'], (x-5, y-7))  # Usa la imagen grande para la barra lateral
            if self.selected_tower == i:
                pg.draw.rect(screen, (255, 255, 255), (x, y, self.tower_width, self.tower_height), 2)  # Marco de selección

            # Dibujar el nombre o el costo de la torre
            text_surface = self.font.render(tower['name'], True, (255, 255, 255))
            screen.blit(text_surface, (x, y + self.tower_height + 5))  # Texto debajo de la torre
