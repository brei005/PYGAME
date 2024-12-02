import pygame as pg
class Animation:
    def __init__(self, image_paths, position, frame_duration=100, loop=True, size=None):
        """
        Clase genérica para manejar animaciones.
        - `image_paths`: Lista de rutas de las imágenes de la animación.
        - `position`: Posición en la pantalla (x, y).
        - `frame_duration`: Duración de cada frame en milisegundos.
        - `loop`: Si la animación debe repetirse (por defecto, True).
        - `size`: Tamaño deseado para las imágenes (ancho, alto). Si es None, se mantiene el tamaño original.
        """
        self.images = [
            pg.transform.scale(pg.image.load(path).convert_alpha(), size) if size else pg.image.load(path).convert_alpha()
            for path in image_paths
        ]
        self.position = position
        self.frame_duration = frame_duration  # Duración de cada frame (en ms)
        self.loop = loop
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.finished = False  # Indica si la animación terminó (para animaciones no cíclicas)

    def update(self):
        """Actualiza el frame actual de la animación."""
        if self.finished:
            return

        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1

            # Si alcanzamos el último frame
            if self.current_frame >= len(self.images):
                if self.loop:
                    self.current_frame = 0  # Reinicia la animación si es cíclica
                else:
                    self.finished = True  # Marca como terminada si no es cíclica
                    self.current_frame = len(self.images) - 1  # Mantén el último frame

    def draw(self, screen):
        """Dibuja el frame actual en la pantalla."""
        if not self.finished:
            screen.blit(self.images[self.current_frame], self.position)
