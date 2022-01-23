import pygame
from pygame.surface import Surface
import config
from local_modules.AudioVisualizer import AudioVisualizer
from local_modules.BaseModule import BaseModule
from local_modules.BindTimer import BindTimer
from local_modules.DrawRectangle import DrawRectangle
from local_modules.Image import Image
from local_modules.MousePosition import MousePosition
from local_modules.MovingGrid import MovingGrid
from local_modules.PolygonDraw import PolygonDraw
from local_modules.PolygonMover import PolygonMover
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
        self.background_color = (35, 7, 45)  # (45, 45, 45)

    def _make_clouds(self):
        screen_rect = self.screen.get_rect()

        import data.polygonCloud

        # CLOUD 1 #
        # cloud filled
        polygon_cloud_filled = PolygonDraw(self.screen)
        polygon_cloud_filled.points = data.polygonCloud.data
        polygon_cloud_filled.color = self.background_color
        polygon_cloud_filled.line_size = 0
        polygon_cloud_filled.calculate()
        self.all_modules.append(polygon_cloud_filled)

        # cloud outline
        polygon_cloud = PolygonDraw(self.screen)
        polygon_cloud.points = data.polygonCloud.data
        polygon_cloud.calculate()
        self.all_modules.append(polygon_cloud)

        polygon_cloud_mover = PolygonMover(
            self.screen, polygon_cloud_filled,
            (-polygon_cloud.get_max_width() + 5, 150),
            (screen_rect.width + 5, 150)
        )
        self.all_modules.append(polygon_cloud_mover)
        polygon_cloud_mover = PolygonMover(
            self.screen, polygon_cloud,
            (-polygon_cloud.get_max_width() + 5, 150),
            (screen_rect.width + 5, 150)
        )
        self.all_modules.append(polygon_cloud_mover)

        # CLOUD 2 #
        # cloud filled
        polygon_cloud_filled = PolygonDraw(self.screen)
        polygon_cloud_filled.points = data.polygonCloud.data
        polygon_cloud_filled.color = self.background_color
        polygon_cloud_filled.line_size = 0
        polygon_cloud_filled.position = (550, 50)
        polygon_cloud_filled.calculate()
        self.all_modules.append(polygon_cloud_filled)

        # cloud outline
        polygon_cloud = PolygonDraw(self.screen)
        polygon_cloud.points = data.polygonCloud.data
        polygon_cloud.position = (550, 50)
        polygon_cloud.calculate()
        self.all_modules.append(polygon_cloud)

        polygon_cloud_mover = PolygonMover(
            self.screen, polygon_cloud_filled,
            (-polygon_cloud.get_max_width() + 5, 50),
            (screen_rect.width + 5, 150)
        )
        polygon_cloud_mover.timer_interval = 0.071
        self.all_modules.append(polygon_cloud_mover)
        polygon_cloud_mover = PolygonMover(
            self.screen, polygon_cloud,
            (-polygon_cloud.get_max_width() + 5, 50),
            (screen_rect.width + 5, 100)
        )
        polygon_cloud_mover.timer_interval = 0.071
        self.all_modules.append(polygon_cloud_mover)

    def import_modules(self):
        import data.fakeFileNames
        screen_rect = self.screen.get_rect()

        # lower background
        lower_background = DrawRectangle(self.screen, 0, 400, 800, 200, (61, 6, 63))
        self.all_modules.append(lower_background)

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

        audio_visualizer = AudioVisualizer(self.screen, 'assets/music/2022-01-09_CyberCyberCyber_wip2.wav')
        self.all_modules.append(audio_visualizer)

        import data.polygonMountains as pM
        mountains_filled = PolygonDraw(self.screen)
        mountains_filled.points = pM.data
        mountains_filled.position = (0, 275)
        mountains_filled.color = self.background_color
        mountains_filled.line_size = 0
        mountains_filled.calculate()
        self.all_modules.append(mountains_filled)

        mountains_filled = PolygonDraw(self.screen)
        mountains_filled.points = pM.data
        mountains_filled.position = (0, 275)
        mountains_filled.line_size = 1
        mountains_filled.calculate()
        self.all_modules.append(mountains_filled)

        skyline_drawer = SkylineCreator(self.screen)
        skyline_drawer.size = (screen_rect.width, skyline_drawer.size[1])
        skyline_drawer.calculate(True)
        self.all_modules.append(skyline_drawer)

        bind_window_timer = BindTimer(self.screen)
        bind_window_timer.timer_interval = 1.2
        bind_window_timer.bind_object(skyline_drawer, 'calculate_windows')
        self.all_modules.append(bind_window_timer)

        self._make_clouds()

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
        mouse_position.color = (255, 144, 31)
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

        # img = pygame.image.load('assets/images/synthwaveSun_small.png')
        # imgRect = img.get_rect()
        # imgRect.x = config.SCREEN_WIDTH / 2 - imgRect.width / 2

        while self.game_is_running:
            # limit frame speed to fps
            self.time_passed = clock.tick(9999)

            self.screen.fill(self.background_color)

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

            # pygame.draw.rect(
            #    self.screen,
            #    (3, 3, 3),
            #    pygame.rect.Rect(0, 0, config.SCREEN_WIDTH, 100)
            # )

            # self.screen.blit(img, imgRect)

            for module in self.all_modules:
                module.timer()
                module.draw()

            fps.render_fps()
            # final draw
            pygame.display.flip()


if __name__ == '__main__':
    gm = GameMaster()
    gm.run()
