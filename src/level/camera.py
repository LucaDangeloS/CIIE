import pygame as pg
from pygame.locals import *

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
 

    def draw_offsetted(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
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

