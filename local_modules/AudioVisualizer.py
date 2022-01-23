# https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file/18625294
# https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator
# https://fairyonice.github.io/implement-the-spectrogram-from-scratch-in-python.html
import struct
import wave
import pygame
from pygame.surface import Surface
from local_modules import BaseModule, Helper


class AudioVisualizer(BaseModule.BaseModule):

    def __init__(self, screen: Surface, audio_file):
        super().__init__(screen)
        self.timer_interval = 0.04
        self.position = (0, 300)
        self.size = (800, 100)
        self.color_left = (255, 41, 117)
        self.color_right = (140, 30, 255)

        self.audio_file = audio_file
        self.wave_file = None  # type: wave.Wave_read or None
        self.frame_rate = 0
        self.frames = 0
        self.frame_index = 0
        self.points_left = []
        self.points_right = []

        self.has_error = False
        self.calculate()

    def calculate(self):
        try:
            self.wave_file = wave.open(self.audio_file, 'r')
            self.frame_rate = self.wave_file.getframerate()
            self.frames = self.wave_file.getnframes()
            self.has_error = False
        except Exception as ex:
            print('AudioVisualizer', ex)
            self.frame_rate = 0
            self.frames = 0
            self.has_error = True

        self.points_left = []
        self.frame_index = 0

    def execute_timer(self):
        if self.has_error:
            return
        # window size / sample rate
        frames_to_sample = self.time_last_execution_diff / self.frame_rate
        #print(frames_to_sample)

        rect = self._screen.get_rect()
        distance_float = frames_to_sample / rect.width
        distance_int = int(distance_float)
        if distance_int <= 0:
            distance_int = 1

        self.points_left.clear()
        self.points_right.clear()

        # add a 1st pos that the polygon can make a clean wrap
        self.points_left.append((self.position[0], self.position[1]))
        self.points_right.append((self.position[0], self.position[1]))
        x = 0
        for x in range(0, rect.width, distance_int):
            wave_data = self.wave_file.readframes(1)
            if not wave_data:
                self.wave_file.rewind()
                break

            # https://docs.python.org/3/library/struct.html#format-characters
            #data = struct.unpack("<2H", wave_data)
            data = struct.unpack("<2h", wave_data)

            data = (
                #Helper.scale_between(data[0], 0, self.size[1], 0, 65535),
                #Helper.scale_between(data[1], 0, self.size[1], 0, 65535)
                Helper.scale_between(data[0], 0, self.size[1], 0, 32767),
                Helper.scale_between(data[1], 0, self.size[1], 0, 32767)
            )

            self.points_left.append((x + self.position[0], data[0] + self.position[1]))
            self.points_right.append((x + self.position[0], data[1] + self.position[1]))

        # add a last pos that the polygon can make a clean wrap
        self.points_left.append((x + 1 + self.position[0], self.position[1]))
        self.points_right.append((x + 1 + self.position[0], self.position[1]))

    def draw(self):
        if self.has_error or len(self.points_left) <= 3:
            return

        pygame.draw.polygon(self._screen, self.color_left, self.points_left, 2)
        pygame.draw.polygon(self._screen, self.color_right, self.points_right, 2)
