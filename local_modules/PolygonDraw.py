import pygame
from pygame.surface import Surface
from local_modules import BaseModule
from local_modules.Helper import rotate_polygon

# resources:
# https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/
# https://www.examplefiles.net/cs/1435025


class PolygonDraw(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.color = (0, 148, 220)
        self.line_size = 2
        self.position = (250, 150)
        # self.points = [(0, 30), (50, 50), (100, 30), (50, 100)]  # different shape
        self.points = [(0, 0), (24, 70), (50, 0), (24, 20)]
        self.points_modified = []

        self.calculate()

    def calculate(self):
        self.points_modified.clear()
        for i in range(len(self.points)):
            position = []
            position.append(self.points[i][0] + self.position[0])
            position.append(self.points[i][1] + self.position[1])

            self.points_modified.append(position)

    def get_max_height(self):
        height = 0
        for point in self.points:
            if point[1] > height:
                height = point[1]

        return height

    def get_max_width(self):
        width = 0
        for point in self.points:
            if point[0] > width:
                width = point[0]

        return width

    def draw(self):
        pygame.draw.polygon(self._screen, self.color, self.points_modified, self.line_size)
