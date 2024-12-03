class Wave:
    def __init__(self, enemies, spawn_rate):
        """
        Inicializa una oleada.
        - `enemies`: Lista de enemigos para la oleada.
        - `spawn_rate`: Tiempo (en segundos) entre el spawn de cada enemigo.
        """
        self.enemies = enemies  # Lista de enemigos para esta oleada
        self.spawn_rate = spawn_rate  # Tiempo entre el spawn de cada enemigo
        self.spawn_timer = 0  # Temporizador para el spawn
        self.index = 0  # Índice del enemigo actual

    def update(self, dt, active_enemies):
        """
        Actualiza la oleada.
        - `dt`: Delta time desde el último frame.
        - `active_enemies`: Lista de enemigos activos en el mapa.
        """
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate and self.index < len(self.enemies):
            # Spawnear un enemigo
            active_enemies.append(self.enemies[self.index])
            self.index += 1
            self.spawn_timer = 0  # Reiniciar el temporizador

    def is_finished(self):
        """
        Verifica si la oleada ha terminado:
        - Todos los enemigos han sido spawneados.
        - No quedan enemigos vivos.
        """
        return (
            self.index >= len(self.enemies)  # Todos los enemigos han sido spawneados
            and all(enemy.is_dead for enemy in self.enemies)  # Todos los enemigos están muertos
        )
