class Player:
    def __init__(self, level):
        """
        Inicializa el jugador.
        - `level`: Nivel actual del juego (influye en los recursos iniciales).
        """
        self.level = level
        self.resources = self.calculate_initial_resources()  # Recursos iniciales basados en el nivel
        self.score = 0  # Puntuación del jugador (opcional, para niveles futuros)

    def calculate_initial_resources(self):
        """
        Calcula los recursos iniciales en función del nivel.
        """
        # Ejemplo: Nivel 1 comienza con 100, cada nivel extra añade 50 recursos
        return 100 + (self.level - 1) * 50

    def add_resources(self, amount):
        """
        Añade recursos al jugador.
        - `amount`: Cantidad de recursos a añadir.
        """
        self.resources += amount
        print(f"Recibiste {amount} recursos. Total: {self.resources}")

    def spend_resources(self, amount):
        """
        Gasta recursos del jugador.
        - `amount`: Cantidad de recursos a gastar.
        - Retorna True si los recursos fueron suficientes, False en caso contrario.
        """
        if self.resources >= amount:
            self.resources -= amount
            print(f"Gastaste {amount} recursos. Recursos restantes: {self.resources}")
            return True
        else:
            print("No tienes suficientes recursos.")
            return False

    def increase_level(self):
        """
        Aumenta el nivel del jugador.
        """
        self.level += 1
        self.resources += self.calculate_initial_resources() // 2  # Bonus por subir de nivel
        print(f"¡Nivel {self.level}! Recursos aumentados: {self.resources}")

    def get_resources(self):
        """
        Retorna los recursos actuales del jugador.
        """
        return self.resources

    def add_score(self, points):
        """
        Añade puntos al jugador.
        - `points`: Cantidad de puntos a añadir.
        """
        self.score += points
        print(f"¡Ganaste {points} puntos! Puntuación total: {self.score}")
