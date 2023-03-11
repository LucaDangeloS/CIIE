import pygame as pg
from entities.entity import Entity


#probably create a general enemy class with a default functionalities and then reinstantiate if needed.
class Enemy(Entity):
    health = 3    

    def __init__(self, collision_sprites, sprite_path, entity_rect, sprite_scale=1):
        super().__init__()
        self.sprite.load_regular_sprites(sprite_path, sprite_scale)
        self.image = self.sprite.get_img(self.state)
        #self.image = pg.image.load('../sprites/players/grandfather/Abuelo.png')
        self.rect = entity_rect

    ''' Observer pattern:
    Define Subject(weapons/attacks) and Obverser(entities) objects.
    When a Subject changes state(there is a collision in attack()), all registered observers are notified and 
     updated automatically (asynchronously if possible)
    '''
    def receive_damage(self, damage_amount):
        self.health -= damage_amount
        print("health_remaining: ", self.health)
        if self.health <= 0: #kill the sprite
            print("DEAD")
            #we should launch the dying animation here
            self.kill()           
    def update(self, state=None):
        self.image = self.sprite.get_img(self.state)
    


    #use the map_matrix checking against TileEnum to know fi there is an obstacle
    def find_path(self, map_matrix, player_pos):
        pass

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,255), self.rect)



