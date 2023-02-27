import pygame as pg
from pygame.locals import *
from scene import SceneInterface
from player import SpriteSheet, Player
from director import Director
from controller import KeyboardController

class Tile(pg.sprite.Sprite):
    #this can be automatically draw by drawing the sprite group I think.
    def __init__(self, pos, groups, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class CameraSpriteGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        #is there a better way to get the size of the screen 
        director = Director() 
        self.half_width = director.screen.get_size()[0] // 2
        self.half_height = director.screen.get_size()[1] // 2
        

        self.offset = pg.math.Vector2()
    
    def draw_offsetted(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

"""
pg.init()
screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True

csprite = CameraSpriteGroup(screen)
print(csprite.half_width, " ", csprite.half_height)

pg.quit()
"""


class Level(SceneInterface):
    def __init__(self, controller):
        self.controller = controller
        self.player = Player('../sprites/granny_movement', 3) #not sure if this should be a parameter
        self.load_graphics() 
 
    def load_graphics(self):
        self.floor_sprites = [ pg.image.load('../sprites/suelo_base.png'), pg.image.load('../sprites/suelo_base_hierbas2.png')]

    def get_map_representation(self, map_representation):#load the csv representation (an external file should be used)
        self.world_map = map_representation
        self.load_map()

    def load_map(self):
        self.floor_tiles = CameraSpriteGroup()
        #we'll use this to calculate collisions, need to specify it in the representation somehow
        self.collision_sprites = pg.sprite.Group()
        for row_idx, row in enumerate(self.world_map):
            for col_idx, value in enumerate(row):
                Tile((col_idx*32, row_idx*32), [self.floor_tiles], self.floor_sprites[value])
        self.floor_tiles.add(self.player)
   
    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(controller):
        self.controller = controller

    def update(self):
        #call the update method on all moving entities
        self.player.update()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        self.floor_tiles.draw_offsetted(self.player, screen)
        self.player.draw(screen)


"""
#Testing a level
world_map = [
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
pg.init()

screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True


controller = KeyboardController()
myLevel = Level(controller)
myLevel.get_map_representation(world_map)

while run:
    clock.tick(60)
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
   
    screen.fill('white')
    myLevel.handle_events(event_list)
    myLevel.update()    
    myLevel.draw(screen)  
    pg.display.update() 



pg.quit()
"""




