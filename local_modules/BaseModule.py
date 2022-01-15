import time
from pygame.surface import Surface


class BaseModule:

    def __init__(self, screen: Surface):
        self._screen = screen
        self.timer_interval = 1.1
        self.__next_calculation_time = time.time()

    def timer(self):
        if self.__next_calculation_time <= time.time():
            self.__next_calculation_time = time.time() + self.timer_interval
            self.execute_timer()

    def calculate(self):
        pass

    def execute_timer(self):
        pass

    def draw(self):
        pass

    def handle_input(self, event):
        pass
