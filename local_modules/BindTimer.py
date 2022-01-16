import pygame
from pygame.surface import Surface
from local_modules import BaseModule


class BindTimer(BaseModule.BaseModule):

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.timer_interval = 0.1

        self._bind_object = None
        self._bind_value_name = None

        self.calculate()

    def bind_object(self, _object, _value_name, execute_instantly=False):
        self._bind_object = _object
        self._bind_value_name = _value_name
        if execute_instantly:
            self.execute_timer()

    def execute_timer(self):
        getattr(self._bind_object, self._bind_value_name)()
