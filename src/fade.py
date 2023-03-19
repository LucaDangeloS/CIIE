from scene import SceneInterface
import pygame as pg

class Fade_in(SceneInterface):
    def __init__(self, screen, fade_speed):
        self.fade = pg.Surface((screen.get_width(), screen.get_height()))
        self.fade_speed = fade_speed

    def draw(self, screen):
        self.fade.fill((0,0,0))
        for alpha in range(0, 300):
            self.fade.set_alpha(alpha)
            screen.blit(self.fade, (0,0))
            pg.display.update()
            pg.time.delay(self.fade_speed)


class Fade_out(SceneInterface):
    def __init__(self, screen, fade_speed):
        self.fade = pg.Surface((screen.get_width(), screen.get_height()))
        self.fade_speed = fade_speed

    def draw(self, screen):
        self.fade.fill((0,0,0))
        for alpha in range(300, 0, -1):
            self.fade.set_alpha(alpha)
            screen.blit(self.fade, (0,0))
            pg.display.update()
            pg.time.delay(self.fade_speed)