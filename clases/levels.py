ENEMIES_BY_LEVEL = {
    1: {  # Nivel 1
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
                "health": 50,
                "speed": 120,
                "damage": 5,
                "count": 5
            }
        ],
        "waves": 3,  # Número de oleadas
        "time_between_waves": 5.0
    }
}
