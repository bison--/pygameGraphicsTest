import pygame
from pygame.surface import Surface
import config
from local_modules.BaseModule import BaseModule
from local_modules.MousePosition import MousePosition
from local_modules.MovingGrid import MovingGrid
from local_modules.RotatingPolygon import RotatingPolygon
from local_modules.UpdateText import UpdateText
from pygameFpsCounter.FpsCounterMax import FpsCounterMax


class GameMaster:

    def __init__(self):
        self.screen = None  # type: Surface or None
        self.time_passed = 0
        self.game_is_running = True
        self.max_fps = 999
        self.all_modules = []  # type: list[BaseModule]

    def import_modules(self):
        from local_modules.TextScroller import TextScroller
        import data.fakeFileNames

        moving_grid = MovingGrid(self.screen)
        moving_grid.position = (-130, config.SCREEN_HEIGHT - 240)
        moving_grid.size = (600, 240)
        moving_grid.timer_interval = 0.01
        moving_grid.calculate()

        #moving_grid = MovingGrid(self.screen)
        #moving_grid.position = (-400, config.SCREEN_HEIGHT - 300)
        #moving_grid.size = (1600, 300)
        #moving_grid.timer_interval = 0.01
        #moving_grid.row_distance = 30
        #moving_grid.calculate()

        self.all_modules.append(moving_grid)

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
        mouse_position.position = (config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 30)
        mouse_position.calculate()
        self.all_modules.append(mouse_position)

        rotating_polygon = RotatingPolygon(self.screen)
        self.all_modules.append(rotating_polygon)

        update_text_rotation_degrees = UpdateText(self.screen)
        update_text_rotation_degrees.color = rotating_polygon.color
        update_text_rotation_degrees.font_size = 20
        update_text_rotation_degrees.timer_interval = 0.25
        update_text_rotation_degrees.position = (rotating_polygon.position[0], rotating_polygon.position[1] + rotating_polygon.get_max_height())
        update_text_rotation_degrees.bind_object(rotating_polygon, 'get_degrees', True)
        self.all_modules.append(update_text_rotation_degrees)

    def run(self):
        pygame.init()
        pygame.display.set_caption("Graphics Test")

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        clock = pygame.time.Clock()

        fps = FpsCounterMax(self.screen)
        fps.color = (38, 127, 0)

        self.import_modules()

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
                    else:
                        for module in self.all_modules:
                            module.handle_input(event)

            #pygame.draw.rect(
            #    self.screen,
            #    (3, 3, 3),
            #    pygame.rect.Rect(0, 0, config.SCREEN_WIDTH, 100)
            #)
            #img = pygame.image.load('assets/images/cybergrid_sky_800.png')
            #self.screen.blit(img, img.get_rect())

            for module in self.all_modules:
                module.timer()
                module.draw()

            fps.render_fps()
            # final draw
            pygame.display.flip()
