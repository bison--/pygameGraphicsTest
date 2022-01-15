import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class TextScroller(BaseModule.BaseModule):

    def __init__(self, screen: Surface, text_lines):
        super().__init__(screen)

        self.text_lines = text_lines
        self.index = 0
        self.text_max_lines = 3

        self.font_size = 50
        self.color = (245, 101, 44)  # orange
        self.position = (0, 10)

        self.font = None  # type: pygame.font or None
        self.__real_position = None  # type: tuple or None
        self.calculate()

    def __get_line_len(self):
        longest = 0
        line_length = 0
        for line in self.text_lines:
            if len(line) > longest:
                longest = len(line)
                line_length = self.font.size(line + ' ')[0]

        return line_length

    def calculate(self):
        self.font = pygame.font.SysFont("MS Comic Sans,Comic Neue", self.font_size)
        self.__real_position = (self.position[0] + (self._screen.get_size()[0] - self.__get_line_len()), self.position[1])

    def execute_timer(self):
        self._render_text()
        self.index += 1
        if self.index >= len(self.text_lines):
            self.index = 0

    def draw(self):
        self._render_text()

    def _render_text(self):
        index_overflow = 0
        draw_position = 0
        draw_index = self.index
        for i in range(self.text_max_lines):
            if draw_index >= len(self.text_lines):
                index_overflow += len(self.text_lines) - 1

            self._screen.blit(
                self.font.render(self.text_lines[draw_index - index_overflow], True, self.color),
                (self.__real_position[0], self.__real_position[1] + (self.font_size * draw_position))
            )

            draw_position += 1
            draw_index += 1
