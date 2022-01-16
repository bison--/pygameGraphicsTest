import pygame
from pygame.surface import Surface
from local_modules import BaseModule
from local_modules.Helper import rotate_polygon

# resources:
# https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/
# https://www.examplefiles.net/cs/1435025


class RotatingPolygon(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.timer_interval = 0.05
        self.degree_change = 2
        self.color = (0, 148, 220)
        self.line_size = 3
        self.position = (250, 150)
        # self.points = [(0, 30), (50, 50), (100, 30), (50, 100)]  # different shape
        self.points = [(0, 0), (24, 70), (50, 0), (24, 20)]
        self.points_modified = []

        self.degrees = 0

        self.calculate()

    def get_degrees(self):
        return abs(self.degrees) % 360

    def calculate(self):
        self.degrees = 0
        self.points_modified.clear()
        for i in range(len(self.points)):
            position = []
            position.append(self.points[i][0] + self.position[0])
            position.append(self.points[i][1] + self.position[1])

            self.points_modified.append(position)

    def execute_timer(self):
        self.degrees += self.degree_change
        self.points_modified = rotate_polygon(self.points_modified, self.degree_change)

    def draw(self):
        pygame.draw.polygon(self._screen, self.color, self.points_modified, self.line_size)
