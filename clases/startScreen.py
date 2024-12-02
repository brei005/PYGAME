import pygame as pg

class StartScreen:
    def __init__(self, screen, font_title, font_option, background_path):
        """
        Clase para manejar la pantalla de inicio.
        - `screen`: Pantalla principal donde se dibuja.
        - `font_title`: Fuente para el título.
        - `font_option`: Fuente para la opción "Start".
        - `background_path`: Ruta de la imagen del fondo.
        """
        self.screen = screen
        self.font_title = font_title
        self.font_option = font_option
        self.title = "VICUNA DEFENSE"
        self.option = "Start"
        self.title_color = (0, 0, 0)  # Color del título
        self.option_color = (0, 0, 0)  # Color de la opción no seleccionada
        self.highlight_color = (0, 255, 0)  # Color de la opción seleccionada
        self.selected = False  # Estado para destacar "Start"
        self.clock = pg.time.Clock()

        # Cargar y escalar la imagen de fondo
        self.background = pg.image.load(background_path).convert()
        self.background = pg.transform.scale(self.background, self.screen.get_size())

    def handle_events(self):
        """
        Maneja los eventos de la pantalla de inicio.
        Retorna True si el jugador selecciona "Start".
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Presionar Enter
                    return True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.is_mouse_over_option():  # Clic sobre "Start"
                    return True
        return False

    def is_mouse_over_option(self):
        """
        Verifica si el mouse está sobre la opción "Start".
        """
        mouse_pos = pg.mouse.get_pos()
        option_surface = self.font_option.render(self.option, True, self.option_color)
        option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        return option_rect.collidepoint(mouse_pos)

    def draw(self):
        """Dibuja la pantalla de inicio."""
        # Dibujar el fondo
        self.screen.blit(self.background, (0, 0))

        # Dibujar el título
        title_surface = self.font_title.render(self.title, True, self.title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(title_surface, title_rect)

        # Dibujar la opción "Start"
        option_surface = self.font_option.render(self.option, True, self.highlight_color if self.is_mouse_over_option() else self.option_color)
        option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(option_surface, option_rect)

        pg.display.flip()

    def show(self):
        """Muestra la pantalla de inicio hasta que se seleccione 'Start'."""
        while True:
            if self.handle_events():  # Verificar si se selecciona "Start"
                break
            self.draw()
            self.clock.tick(60)
