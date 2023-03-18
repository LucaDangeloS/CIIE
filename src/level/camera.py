import pygame as pg
from pygame.locals import *
from entities.entity import Entity

class CameraSpriteGroup(pg.sprite.Group):
    screen_res = None
    def __init__(self, screen_resolution):
        super().__init__()
        self.screen_res = screen_resolution
        self.screen_rect = Rect(0,0,self.screen_res[0], self.screen_res[1])
        self.half_width = screen_resolution[0] // 2
        self.half_height = screen_resolution[1] // 2
        
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

    def draw_offsetted(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset - (sprite.image_offset if isinstance(sprite, Entity) else pg.math.Vector2(0, 0))
            screen.blit(sprite.image, offset_pos)
        #for sprite in self.sprites():
            ##screen.blit(sprite.image, sprite.rect)
    
    def draw_offsetted_throwables(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
            if not self.screen_rect.collidepoint(offset_pos):
                sprite.kill()

