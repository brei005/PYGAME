ENEMIES_BY_LEVEL = {
    1: {  # Nivel 1
        "terrain_texture": "assets/maps/level1_texture.png",  # Textura del terreno para el nivel 1
        "enemies": [
            {
                "frames_by_direction": {
                    "up": [
                        "assets/enemies/1/up/enemigo1_arriba_der_1.png",
                        "assets/enemies/1/up/enemigo1_arriba_der_2.png",
                        "assets/enemies/1/up/enemigo1_arriba_der_3.png",
                    ],
                    "down": [
                        "assets/enemies/1/down/enemigo1_abajo_izq_1.png",
                        "assets/enemies/1/down/enemigo1_abajo_izq_2.png",
                        "assets/enemies/1/down/enemigo1_abajo_izq_3.png",
                    ],
                    "left": [
                        "assets/enemies/1/left/enemigo1_arriba_izq_1.png",
                        "assets/enemies/1/left/enemigo1_arriba_izq_2.png",
                        "assets/enemies/1/left/enemigo1_arriba_izq_3.png",
                    ],
                    "right": [
                        "assets/enemies/1/right/enemigo1_abajo_der_1.png",
                        "assets/enemies/1/right/enemigo1_abajo_der_2.png",
                        "assets/enemies/1/right/enemigo1_abajo_der_3.png",
                    ],
                },
                "reward": 10,
                "health": 10,
                "speed": 200,
                "damage": 5,
                "count": 3
            }
        ],
        "waves": 2,  # Número de oleadas
        "time_between_waves": 0.5
    },
    2: {  # Nivel 2
        "terrain_texture": "assets/maps/level2_texture.png",  # Textura del terreno para el nivel 2
        "enemies": [
            {
                "frames_by_direction": {
                    "up": [
                        "assets/enemies/2/up/enemigo2_arriba_der_1.png",
                        "assets/enemies/2/up/enemigo2_arriba_der_2.png",
                        "assets/enemies/2/up/enemigo2_arriba_der_3.png",
                    ],
                    "down": [
                        "assets/enemies/2/down/enemigo2_abajo_izq_1.png",
                        "assets/enemies/2/down/enemigo2_abajo_izq_2.png",
                        "assets/enemies/2/down/enemigo2_abajo_izq_3.png",
                    ],
                    "left": [
                        "assets/enemies/2/left/enemigo2_arriba_izq_1.png",
                        "assets/enemies/2/left/enemigo2_arriba_izq_2.png",
                        "assets/enemies/2/left/enemigo2_arriba_izq_3.png",
                    ],
                    "right": [
                        "assets/enemies/2/right/enemigo2_abajo_der_1.png",
                        "assets/enemies/2/right/enemigo2_abajo_der_2.png",
                        "assets/enemies/2/right/enemigo2_abajo_der_3.png",
                    ],
                },
                "reward": 20,
                "health": 10,
                "speed": 120,
                "damage": 10,
                "count": 2
            }
        ],
        "waves": 2,
        "time_between_waves": 1.0
    },
    3: {  # Nivel 3
        "terrain_texture": "assets/maps/level3_texture.png",  # Textura del terreno para el nivel 3
        "enemies": [
            {
                "frames_by_direction": {
                    "up": [
                        "assets/enemies/3/up/enemigo3_arriba_der_1.png",
                        "assets/enemies/3/up/enemigo3_arriba_der_2.png",
                        "assets/enemies/3/up/enemigo3_arriba_der_3.png",
                    ],
                    "down": [
                        "assets/enemies/3/down/enemigo3_abajo_izq_1.png",
                        "assets/enemies/3/down/enemigo3_abajo_izq_2.png",
                        "assets/enemies/3/down/enemigo3_abajo_izq_3.png",
                    ],
                    "left": [
                        "assets/enemies/3/left/enemigo3_arriba_izq_1.png",
                        "assets/enemies/3/left/enemigo3_arriba_izq_2.png",
                        "assets/enemies/3/left/enemigo3_arriba_izq_3.png",
                    ],
                    "right": [
                        "assets/enemies/3/right/enemigo3_abajo_der_1.png",
                        "assets/enemies/3/right/enemigo3_abajo_der_2.png",
                        "assets/enemies/3/right/enemigo3_abajo_der_3.png",
                    ],
                },
                "reward": 30,
                "health": 10,
                "speed": 180,
                "damage": 15,
                "count": 2
            }
        ],
        "waves": 1,
        "time_between_waves": 1.0
    }
}
