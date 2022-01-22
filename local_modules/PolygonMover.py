import pygame
from pygame.surface import Surface
from local_modules import BaseModule
from local_modules.Helper import rotate_polygon


# resources:
# https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/
# https://www.examplefiles.net/cs/1435025


class PolygonMover(BaseModule.BaseModule):

    def __init__(self, screen: Surface, polygon, end_position=(0, 0), start_position=None):
        super().__init__(screen)
        self.start_position = start_position
        self.end_position = end_position
        self.polygon = polygon
        self.timer_interval = 0.05

    def execute_timer(self):
        # todo: make it more complete!

        pos = self.polygon.position

        if pos[0] == self.end_position[0] and pos[1] == self.end_position[1]:
            if self.start_position is not None:
                pos = (self.start_position[0] + 1, self.start_position[1] + 1)
            else:
                return

        pos = [pos[0] - 1, pos[1] - 1]

        if pos[0] < self.end_position[0]:
            pos[0] = self.end_position[0]
        if pos[1] < self.end_position[1]:
            pos[1] = self.end_position[1]

        self.polygon.position = tuple(pos)
        self.polygon.calculate()


