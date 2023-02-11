import pygame as pg
from pygame.locals import *

WIDTH =  1280
HEIGHT = 720
FPS = 60
TILESIZE = 64



class Player(pg.sprite.Sprite):
    run = False
    walking_speed = 3 
    running_speed = 5
    direction = pg.math.Vector2()
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group) #adds this sprite to all sprite groups in groups
        self.image = pg.image.load('./adventurer_idle.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)
         
        self.collision_sprites = collision_sprites

    def controller_input(self, event):
        #controller
        if event.type == JOYHATMOTION:
            self.direction.x = event.value[0]
            self.direction.y = -event.value[1]
        elif event.type == JOYBUTTONDOWN:
            if event.button == 5:
                self.run = True
        elif event.type == JOYBUTTONUP:
            if event.button == 5:
                self.run = False


    #This way of taking input causes weird behavior when you release two keys that have been pressed
    #simultaneously, it makes the character wiggle when it should not
    #It's very minimal but we may need to fix it (it happens in diagonal movements)
    #To clearly see it press left then right, and then release at the same time
    
    #I prefer to check for the events rather than using key.get_pressed()
    #with key.get_pressed lose precision on the order of key activations
    def input(self, event, incr): 
        #keyboard
        if event.key == K_UP or event.key == K_w:
            self.direction.y += -incr
        if event.key == K_DOWN or event.key == K_s:
            self.direction.y += incr

        if event.key == K_RIGHT or event.key == K_d:
            self.direction.x += incr
        if event.key == K_LEFT or event.key == K_a:
            self.direction.x -= incr

        if event.key == K_LSHIFT:
            self.run = (incr > 0) #to get true if keydown or false if keyup


    def move(self):
        move = self.direction
        if self.direction.magnitude() != 0:
            move = self.direction.normalize()
        
        if self.run:
            self.rect.x += move.x * self.running_speed
            self.collision('horizontal')
            self.rect.y += move.y * self.running_speed
            self.collision('vertical')
        else:
            self.rect.x += move.x * self.walking_speed
            self.collision('horizontal')
            self.rect.y += move.y * self.walking_speed
            self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            # can this be optimized?
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: #right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: #left
                        self.rect.left = sprite.rect.right
        elif direction == 'vertical':
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: #right
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: #left
                        self.rect.top = sprite.rect.bottom
    def update(self):
        self.move()




class Tile(pg.sprite.Sprite): #example of a game asset
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.image.load('./tile_42.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)




class Level:
    def __init__(self):
         #with this we can get the display surface from any point in the class
        self.display_surface = pg.display.get_surface()

        self.visible_sprites = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()

    def create_map(self): #we should have a matrix representation of the map
        self.player = Player((100,100), [self.visible_sprites], self.collision_sprites)
        
        #we don't need to save a reference because it's in the groups
        Tile((200,200), [self.visible_sprites, self.collision_sprites]) 
    
    def run(self):
        for event in pg.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                self.player.input(event, 1)
            elif event.type == KEYUP:
                self.player.input(event, -1)
            else:
                self.player.controller_input(event)
    

        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        return True








pg.init()
pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
run = True

level = Level()
level.create_map()

while run:
    screen.fill('black') 

    run = level.run()

    pg.display.update()
    clock.tick(FPS)




pg.quit()















