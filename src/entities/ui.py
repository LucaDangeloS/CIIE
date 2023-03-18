import pygame as pg
from pygame.locals import *
from entities.sprites import SpriteSheet

class UIElement(pg.sprite.Sprite):
    image = None
    rect = None
    def __init__(self, spritesheet_path:str, spr_size:tuple[int,int], scale=1):
        super().__init__()
        spritesheet = SpriteSheet(pg.image.load(spritesheet_path))
        self.image_list = spritesheet.load_tiled_style(spr_size, scale)

    def draw(self, screen): #this is probably done throw sprite groups
        screen.blit(self.image, self.rect)

    def update(self):
        raise NotImplementedError 


class PlayerHealthUI(UIElement):
    def __init__(self, max_health, scale=1):
        super().__init__('../sprites/interface/hearts-sheet.png', (16,16), scale)
        self.rect = pg.Rect(20,10, 40*scale, 20*scale)
        
        #needed to dictate the total amount of hearts displayed 
        self.max_health = max_health
        self.update(max_health)

    #generates the actual image with regards to the health amount
    def update(self, health_amount):
        surface = pg.Surface((self.rect.w, self.rect.h), SRCALPHA, 32)

        for i in range(round((self.max_health/2)+0.1)): #amount of hearts displayed
            x = i * (self.rect.w / round((self.max_health/2)+0.1))
            if health_amount >= 2: #draw full heart
                surface.blit(self.image_list[0], (x, self.rect.y))
                health_amount -= 2
            elif health_amount == 1:
                surface.blit(self.image_list[1], (x, self.rect.y))
                health_amount -= 1
            else:
                surface.blit(self.image_list[2], (x, self.rect.y))
        
        self.image = surface


class ClockUI(UIElement):
    def __init__(self, screen_res:tuple[int, int], scale=1):
        self.scale = scale
        self.sprt_size = (32,32)
        super().__init__('../sprites/interface/clock-sheet.png', self.sprt_size, scale)
        
        
        #x = screen_res[0] - self.sprt_size[0] * (self.scale) 
        x = self.sprt_size[0] // 2
        y = screen_res[1] - self.sprt_size[1] * (self.scale)
        self.rect = pg.Rect(x, y, self.sprt_size[0]*self.scale, self.sprt_size[1]*self.scale)
        self.image = self.image_list[-1]

    def update_screen_res(self, screen_res:tuple[int,int]):
        self.rect.x = screen_res[0] - self.sprt_size[0] * (self.scale+2) 
        self.rect.y = screen_res[1] - self.sprt_size[1] * (self.scale+2)

    def update(self, used_percentage:float):

        imgs_perctenage =  1 / (len(self.image_list)-1)
        #choose the image based on the used_percentage of the list
        inversed = (len(self.image_list)-1) - int(used_percentage//imgs_perctenage)
        self.image = self.image_list[inversed]

