import pygame as pg
from entities.entity import Entity


#probably create a general enemy class with a default functionalities and then reinstantiate if needed.
class Enemy(Entity):
    health = 2

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
        if self.health <= 0: #kill the sprite
            #we should launch the dying animation here
            self.kill()          

    def update(self, state=None):
        self.image = self.sprite.get_img(self.state)
        # goal = self.behavior.get_goal()


    #use the map_matrix checking against TileEnum to know fi there is an obstacle
    def find_path(self, map_matrix, player_pos):
        pass

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,255), self.rect)



# class Enemy:
#     def __init__(self, map, player_pos):
#         self.map = map
#         self.player_pos = player_pos
#         self.path = []

#     def update(self):
#         if len(self.path) == 0:
#             self.path = astar(self.map, self.get_current_pos(), self.player_pos)
        
#         if len(self.path) > 0:
#             next_pos = self.path.pop(0)
#             self.move_to(next_pos)
        

#     def get_current_pos(self):
#         # your implementation here, e.g. using the enemy's coordinates on the map

#     def move_to(self, position):
#         # your implementation here, e.g. moving the enemy to a specific position on the map
