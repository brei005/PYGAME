from clases.enemy import AnimatedEnemy
from clases.wave import Wave

def get_waves_for_level(level, path):
    """
    Devuelve las oleadas para un nivel específico usando AnimatedEnemy.
    """
    if level == 1:
        return [
            Wave(
                enemies=[
                    AnimatedEnemy(
                        grid_path=path,
                        animation_frames=[
                            "assets/enemies/1/arriba_der/enemigo1_arriba_der_1.png",
                            "assets/enemies/1/arriba_der/enemigo1_arriba_der_2.png",
                            "assets/enemies/1/arriba_der/enemigo1_arriba_der_3.png"
                        ],
                        reward=10,
                        health=100,
                        speed=30,
                        damage=10
                    )
                    for _ in range(7)
                ],
                spawn_rate=2.0  # Un enemigo cada 2 segundos
            )
        ]
    elif level == 2:
        return [
            Wave(
                enemies=[
                    AnimatedEnemy(
                        grid_path=path,
                        animation_frames=[
                            "enemies/enemy2_frame1.png",
                            "enemies/enemy2_frame2.png",
                            "enemies/enemy2_frame3.png"
                        ],
                        reward=15,
                        health=150,
                        speed=25,
                        damage=15
                    )
                    for _ in range(8)
                ],
                spawn_rate=1.5  # Un enemigo cada 1.5 segundos
            )
        ]
    elif level == 3:
        return [
            Wave(
                enemies=[
                    AnimatedEnemy(
                        grid_path=path,
                        animation_frames=[
                            "enemies/enemy3_frame1.png",
                            "enemies/enemy3_frame2.png",
                            "enemies/enemy3_frame3.png"
                        ],
                        reward=20,
                        health=200,
                        speed=20,
                        damage=20
                    )
                    for _ in range(10)
                ],
                spawn_rate=1.0  # Un enemigo cada segundo
            )
        ]
    else:
        raise ValueError(f"Nivel {level} no está configurado.")
