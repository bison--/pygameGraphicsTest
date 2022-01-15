import pygame
from pygame.surface import Surface
from local_modules import BaseModule
import random


class SkylineCreator(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        #self.timer_interval = 0.1
        self.primary_color = (20, 7, 61)
        self.window_color = (248, 154, 25)
        self.position = (0, 400)
        self.size = (800, 80)
        self.add_windows = True
        self.window_probability = 20

        self.skyline_buildings = []  # type: list[pygame.rect.Rect]
        self.building_windows = []  # type: list[pygame.rect.Rect]

        self.calculate()

    def draw(self):
        count = 0
        for rect in self.skyline_buildings:
            color_shade = [self.primary_color[0], self.primary_color[1], self.primary_color[2] + count]

            if color_shade[2] > 255:
                count = 0
                color_shade[2] = self.primary_color[2]

            pygame.draw.rect(
                self._screen,
                color_shade,
                rect
            )
            count += 2

        for rect in self.building_windows:
            pygame.draw.rect(
                self._screen,
                self.window_color,
                rect
            )

    def calculate(self):
        x_drawer = 0
        while x_drawer < self.size[0]:
            x_drawer = self.create_building(x_drawer)

    def create_building(self, x_offset):
        width = random.randint(int(self.size[0] / 30), int(self.size[0] / 20))
        height = random.randint(int(self.size[1] / 10), int(self.size[1] + self.size[1] / 10))
        building_rect = pygame.rect.Rect(x_offset, self.position[1] - height, width, height)
        self.skyline_buildings.append(building_rect)

        if self.add_windows:
            window_width = int(width / 10)
            window_height = int(height / 10)

            for row in range(building_rect.y + 5, (building_rect.y + building_rect.height) - window_height, window_height + 5):
                for col in range(building_rect.x + 5, (building_rect.x + building_rect.width) - window_width, window_width + 5):
                    if self.window_probability >= random.randint(0, 100):
                        self.building_windows.append(
                            pygame.rect.Rect(col, row, window_width, window_height)
                        )

        return x_offset + width



