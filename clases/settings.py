# settings.py
RES = (900, 700)
FPS = 60
INICIO_X=160
INICIO_Y=80
GAP_x = 1  # Espacio horizontal entre bloques
GAP_y = 1  # Espacio vertical entre bloques
DISPLAY_SIZE = (350, 300)
BLOCK_WIDTH = 10  # Ancho de cada bloque
BLOCK_HEIGHT = 5  # Alto de cada bloque
# Tipos de terreno y texturas
TERRAIN_TYPES = {
    0: 'assets/pasto.png',  # Terreno por defecto
    1: 'assets/camino.png',  # Camino para enemigos
    2: 'assets/base.png'     # Terreno para la base
}