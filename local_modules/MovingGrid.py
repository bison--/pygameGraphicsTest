import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class MovingGrid(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.timer_interval = 0.1
        self.primary_color = (242, 34, 255)  # (255, 0, 220)
        self.position = (250, 150)
        self.size = (400, 240)
        self.row_distance = 24
        self.timer_ticks = 0

        self.rows = []
        self.lower_bound = 0
        self.hide_color = (45, 45, 45)  # type: tuple or None

        self.calculate()

    def calculate(self):
        #self.lower_bound = self.position[1] + self.size[1] - ((self.position[1] + self.size[1]) % self.row_distance)
        self.lower_bound = self.position[1] + self.size[1]

        self.rows.clear()
        for y_position in range(self.position[1], self.lower_bound, self.row_distance):
            self.rows.append(y_position)

    def execute_timer(self):
        self.timer_ticks += 1

        # re-calculate
        for i in range(len(self.rows)):
            self.rows[i] += 1

        # move last out-of-bounds element back to top
        for i in range(len(self.rows)):
            if self.rows[i] >= self.lower_bound:
                self.rows[i] = self.position[1]
                self.rows.insert(0, self.rows.pop())
                break

    def draw(self):
        iteration_count = 0
        for y_position in self.rows:
            start_position = (self.position[0], y_position)
            end_position = (self.position[0] + self.size[0], y_position)
            pygame.draw.line(self._screen, self.primary_color, start_position, end_position, width=1 + int(iteration_count / 2))
            iteration_count += 1

        # center line
        lower_center = (self.position[0] + (self.size[0] / 2), self.lower_bound)
        upper_center = (self.position[0] + (self.size[0] / 2), self.position[1])
        pygame.draw.line(
            self._screen, self.primary_color,
            lower_center, upper_center,
            width=2
        )

        # right
        iteration_count = 0
        end_position = ()
        for x_position in range(int(lower_center[0]), self.position[0] + self.size[0], self.row_distance):
            start_position = (x_position, self.lower_bound)
            end_position = (x_position - (iteration_count * self.row_distance / 2), self.position[1])
            pygame.draw.line(self._screen, self.primary_color, start_position, end_position, width=2)  # + int(iteration_count / 2)
            iteration_count += 1

        self.draw_hide_box(
            end_position[0] + self.row_distance,
            end_position[1],
            self.position[0] + self.size[0] - end_position[0],
            self.size[1] + self.row_distance
        )

        # left
        iteration_count = 0
        start_position = ()
        for x_position in range(int(lower_center[0]), self.position[0], -self.row_distance):
            start_position = (x_position, self.lower_bound)
            end_position = (x_position + (iteration_count * self.row_distance / 2), self.position[1])
            pygame.draw.line(self._screen, self.primary_color, start_position, end_position, width=2)  # + int(iteration_count / 2)
            iteration_count += 1

        self.draw_hide_box(
            self.position[0] - self.row_distance,
            self.position[1],
            end_position[0] - self.position[0],
            self.size[1] + self.row_distance
        )

        # iteration_count = 0
        # for y_position in range(self.size[1], self.position[1] + self.size[1], self.row_distance):
        #     y_offset = self.position[1] + y_position + self.timer_ticks
        #     start_position = (self.position[0], y_offset)
        #     end_position = (self.position[0] + self.size[0], y_offset)
        #     pygame.draw.line(self._screen, self.primary_color, start_position, end_position, width=1 + int(iteration_count / 2))
        #     iteration_count += 1

    def draw_hide_box(self, x, y, width, height):
        if self.hide_color is None:
            return

        pygame.draw.rect(
            self._screen,
            self.hide_color,
            pygame.rect.Rect(x, y, width, height)
        )
