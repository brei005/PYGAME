RES = (900, 700)
FPS = 60
INICIO_X = 160
INICIO_Y = 80
GAP_x = 1  # Espacio horizontal entre bloques
GAP_y = 1  # Espacio vertical entre bloques
DISPLAY_SIZE = (350, 300)
BLOCK_WIDTH = 10  # Ancho de cada bloque
BLOCK_HEIGHT = 5  # Alto de cada bloque

# Texturas generales para los tipos de terreno
FIXED_TERRAIN_TYPES = {
    '1': 'assets/piedra.png',   # Camino (fijo)
    '2': 'assets/base.png',   # Base (fijo)
    'x': 'assets/piedra.png'   # Inicio (fijo)
}

# Texturas de terreno vacío ('0') por nivel
LEVEL_SPECIFIC_TERRAIN = {
    1: 'assets/maps/level1_texture.png',  # Textura de '0' para el nivel 1
    2: 'assets/maps/level2_texture.png',  # Textura de '0' para el nivel 2
    3: 'assets/maps/level3_texture.png'   # Textura de '0' para el nivel 3
}
