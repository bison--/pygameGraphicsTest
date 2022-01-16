import pygame
from pygame.surface import Surface
from local_modules import BaseModule
from local_modules.Helper import rotate_polygon


class RotatingPolygon(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.timer_interval = 0.1
        self.color = (0, 148, 220)
        self.position = (250, 150)
        self.points = [(0, 30), (50, 0), (100, 30), (50, 100)]
        self.points_modified = []

        self.degrees = 0

        self.calculate()

    def calculate(self):
        self.points_modified.clear()
        for i in range(len(self.points)):
            position = []
            position.append(self.points[i][0] + self.position[0])
            position.append(self.points[i][1] + self.position[1])

            self.points_modified.append(position)

    def execute_timer(self):
        self.degrees += 1
        self.points_modified = rotate_polygon(self.points_modified, self.degrees)

    def draw(self):
        pygame.draw.polygon(self._screen, self.color, self.points_modified, 4)



#https://ukdevguy.com/tutorial-on-how-to-draw-shapes-in-pygame/
#https://www.examplefiles.net/cs/1435025
#points = [(350, 350), (400, 320), (460, 340), (410, 450)]
#pygame.draw.polygon(game_window, (0,0,255), points, 4)

