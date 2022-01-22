import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class DrawRectangle(BaseModule.BaseModule):

    def __init__(self, screen: Surface, x, y, width, height, color=(12, 34, 56)):
        super().__init__(screen)
        self.position = (x,  y)
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.draw_box()

    def draw_box(self):
        pygame.draw.rect(
            self._screen,
            self.color,
            pygame.rect.Rect(self.position[0], self.position[1], self.width, self.height)
        )
