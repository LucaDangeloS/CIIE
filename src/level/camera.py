import pygame as pg
from pygame.locals import *
from entities.entity import Entity

class CameraSpriteGroup(pg.sprite.Group):
    screen_res = None
    map_limit = None

    @classmethod
    def set_map_limit(cls, limit):
        cls.map_limit = limit

    def __init__(self, screen_resolution):
        super().__init__()
        self.screen_res = screen_resolution
        self.screen_rect = Rect(0,0,self.screen_res[0], self.screen_res[1])
        self.half_width = screen_resolution[0] // 2
        self.half_height = screen_resolution[1] // 2
        self.curr_half_width = self.half_width
        self.curr_half_height = self.half_height

        self.offset = pg.math.Vector2()
    
    def update_screen_resolution(self, res):
        self.screen_res = res 
        self.screen_rect = Rect(0,0,self.screen_res[0], self.screen_res[1])
        
    def debug_draw(self, player, screen, rect, color='red'):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        offset_pos = rect.topleft - self.offset
        tmp_rect = rect.copy()
        tmp_rect[0] = offset_pos[0]
        tmp_rect[1] = offset_pos[1]
        pg.draw.rect(screen, pg.Color(color), tmp_rect, 2)

    def get_camera_offset(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        if self.offset.x < 0:
            self.offset.x = 0
        elif self.offset.x > self.map_limit[0] - self.screen_res[0]:
            self.offset.x = self.map_limit[0] - self.screen_res[0]
        if self.offset.y < 0:
            self.offset.y = 0
        elif self.offset.y > self.map_limit[1] - self.screen_res[1]:
            self.offset.y = self.map_limit[1] - self.screen_res[1]

        
    def draw_offsetted(self, player, screen):
        self.get_camera_offset(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset - (sprite.image_offset if isinstance(sprite, Entity) else pg.math.Vector2(0, 0))
            screen.blit(sprite.image, offset_pos)
        #for sprite in self.sprites():
            ##screen.blit(sprite.image, sprite.rect)
    
    def draw_offsetted_throwables(self, player, screen):
        self.get_camera_offset(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
            if not self.screen_rect.collidepoint(offset_pos):
                sprite.kill()

