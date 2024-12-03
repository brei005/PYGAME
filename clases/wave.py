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
        """
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate and self.index < len(self.enemies):
            # Spawnear un enemigo
            enemy = self.enemies[self.index]
            if enemy.path_index == 0:  # Solo añadir si aún no está activo
                active_enemies.append(enemy)
            self.index += 1
            self.spawn_timer = 0


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
