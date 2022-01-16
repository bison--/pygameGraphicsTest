import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class Image(BaseModule.BaseModule):

    def __init__(self, screen: Surface, _image):
        super().__init__(screen)
        self.position = (0, 0)

        self.img = pygame.image.load(_image)
        self.img_rect = self.img.get_rect()
        self.img_draw_rect = self.img.get_rect().copy()

        self.center_width_rect = None  # type: pygame.Rect or None
        self.center_height_rect = None  # type: pygame.Rect or None

        self.calculate()

    def set_center_rect(self, rect):
        self.center_width_rect = rect
        self.center_height_rect = rect
        self.calculate()

    def set_center_width_rect(self, rect):
        self.center_width_rect = rect
        self.calculate()

    def set_center_height_rect(self, rect):
        self.center_height_rect = rect
        self.calculate()

    def calculate(self):
        self.img_draw_rect = self.img.get_rect().copy()

        if self.center_width_rect is not None:
            self.img_draw_rect.x = self.center_width_rect.width / 2 - self.img_draw_rect.width / 2

        if self.center_height_rect is not None:
            self.img_draw_rect.y = self.center_width_rect.height / 2 - self.img_draw_rect.height / 2

    def draw(self):
        self._screen.blit(self.img, self.img_draw_rect)
