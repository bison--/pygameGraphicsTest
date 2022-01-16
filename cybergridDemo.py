import pygame
from pygame.surface import Surface
import config
from local_modules.BaseModule import BaseModule
from local_modules.BindTimer import BindTimer
from local_modules.Image import Image
from local_modules.MousePosition import MousePosition
from local_modules.MovingGrid import MovingGrid
from local_modules.SkylineCreator import SkylineCreator
from local_modules.TextScroller import TextScroller
from pygameFpsCounter.FpsCounterMax import FpsCounterMax


class GameMaster:

    def __init__(self):
        self.screen = None  # type: Surface or None
        self.time_passed = 0
        self.game_is_running = True
        self.max_fps = 999
        self.all_modules = []  # type: list[BaseModule]

    def import_modules(self):
        import data.fakeFileNames
        screen_rect = self.screen.get_rect()

        sun = Image(self.screen, 'assets/images/synthwaveSun_small.png')
        sun.set_center_width_rect(self.screen.get_rect())
        self.all_modules.append(sun)

        moving_grid = MovingGrid(self.screen)
        moving_grid.position = (-400, screen_rect.height - 200)
        moving_grid.size = (1600, 240)
        moving_grid.timer_interval = 0.01
        moving_grid.row_distance = 60
        moving_grid.calculate()
        self.all_modules.append(moving_grid)

        skyline_drawer = SkylineCreator(self.screen)
        skyline_drawer.size = (screen_rect.width, skyline_drawer.size[1] + 100)
        skyline_drawer.calculate(True)
        self.all_modules.append(skyline_drawer)

        bind_window_timer = BindTimer(self.screen)
        bind_window_timer.timer_interval = 1.2
        bind_window_timer.bind_object(skyline_drawer, 'calculate_windows')
        self.all_modules.append(bind_window_timer)

        text_scroller = TextScroller(self.screen, data.fakeFileNames.fakeFileNames)
        text_scroller.color = (38, 127, 0)
        text_scroller.font_size = 23
        text_scroller.text_max_lines = 3
        text_scroller.timer_interval = .4
        text_scroller.calculate()
        self.all_modules.append(text_scroller)

        text_scroller2 = TextScroller(self.screen, data.fakeFileNames.fakeFileNames)
        text_scroller2.color = (38, 127, 0)
        text_scroller2.font_size = 12
        text_scroller2.text_max_lines = 3
        text_scroller2.timer_interval = .1
        text_scroller2.position = (-720, 550)
        text_scroller2.calculate()
        self.all_modules.append(text_scroller2)

        mouse_position = MousePosition(self.screen)
        mouse_position.font_size = 30
        mouse_position.position = (screen_rect.width - 100, screen_rect.height - 30)
        mouse_position.calculate()
        self.all_modules.append(mouse_position)

    def run(self):
        pygame.init()
        pygame.display.set_caption("Graphics Test CyberGrid Demo")

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        clock = pygame.time.Clock()

        fps = FpsCounterMax(self.screen)
        fps.color = (38, 127, 0)

        self.import_modules()

        #img = pygame.image.load('assets/images/synthwaveSun_small.png')
        #imgRect = img.get_rect()
        #imgRect.x = config.SCREEN_WIDTH / 2 - imgRect.width / 2

        while self.game_is_running:
            # limit frame speed to fps
            self.time_passed = clock.tick(9999)

            self.screen.fill((45, 45, 45))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_is_running = False
                    elif event.key == pygame.K_c:
                        for module in self.all_modules:
                            module.calculate()
                    elif event.key == pygame.K_r:
                        self.all_modules.clear()
                        self.import_modules()
                    else:
                        for module in self.all_modules:
                            module.handle_input(event)

            #pygame.draw.rect(
            #    self.screen,
            #    (3, 3, 3),
            #    pygame.rect.Rect(0, 0, config.SCREEN_WIDTH, 100)
            #)

            #self.screen.blit(img, imgRect)

            for module in self.all_modules:
                module.timer()
                module.draw()

            fps.render_fps()
            # final draw
            pygame.display.flip()


if __name__ == '__main__':
    gm = GameMaster()
    gm.run()
