import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class MousePosition(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.timer_interval = 0.050
        self.font_size = 50
        self.color = (245, 101, 44)  # orange
        self.position = (0, 10)
        self.font = None  # type: pygame.font or None
        self.mouse_position_text = '1000 x 1000'

        self.calculate()

    def get_line_len(self):
        return self.font.size(self.mouse_position_text + ' ')[0]

    def calculate(self):
        self.font = pygame.font.SysFont("MS Comic Sans,Comic Neue", self.font_size)

    def execute_timer(self):
        self.mouse_position_text = f"{pygame.mouse.get_pos()[0]} x {pygame.mouse.get_pos()[1]}"
        self._render_text()

    def draw(self):
        self._render_text()

    def _render_text(self):
        self._screen.blit(
            self.font.render(self.mouse_position_text, True, self.color),
            self.position
        )
