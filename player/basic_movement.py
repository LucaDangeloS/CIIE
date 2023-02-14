import pygame as pg
from pygame.locals import *

WIDTH =  1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
class SpriteSheet(): #should reimplement this using sprite.Sprite
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pg.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pg.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

class Player(pg.sprite.Sprite):
    animation_idx = 0
    walking_speed = 4 
    running_speed = 6 
    direction = pg.math.Vector2()
    motion = {"up": False, "right": False, "down": False, "left": False, "run": False}
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group) #adds this sprite to all sprite groups in groups
        self.image = front_granny[0]
        self.rect = self.image.get_rect(topleft = pos)
         
        self.collision_sprites = collision_sprites

    def controller_input(self, event):
        if event.type == JOYHATMOTION:
            print("0: ", event.value[0])
            print("1: ", event.value[1])
            if event.value[0] == 1:
                self.motion['right'] = True
                self.motion['left'] = False
            elif event.value[0] == -1:
                self.motion['left'] = True
                self.motion['right'] = False
            elif event.value[0] == 0:
                self.motion['left'] = False
                self.motion['right'] = False

            if event.value[1] == 1:
                self.motion['down'] = False
                self.motion['up'] = True
            elif event.value[1] == -1:
                self.motion['up'] = False
                self.motion['down'] = True
            elif event.value[1] == 0:
                self.motion['down'] = False
                self.motion['up'] = False


            #self.direction.x = event.value[0]
            #self.direction.y = -event.value[1]
        elif event.type == JOYBUTTONDOWN:
            if event.button == 5:
                self.motion['run'] = True
        elif event.type == JOYBUTTONUP:
            if event.button == 5:
                self.motion['run'] = False

        self.apply_input()

    def apply_input(self):
        if self.motion['up'] and not self.motion['down']:
            self.image = back_granny[self.animation_idx]
            self.direction.y = -1
        elif not self.motion['up'] and self.motion['down']:
            self.image = front_granny[self.animation_idx]
            self.direction.y = 1
        else:
            self.image = front_granny[self.animation_idx]
            self.direction.y = 0

        if self.motion['right'] and not self.motion['left']:
            self.image = right_granny[self.animation_idx]
            self.direction.x = 1
        elif not self.motion['right'] and self.motion['left']:
            self.image = left_granny[self.animation_idx]
            self.direction.x = -1
        else:
            self.direction.x = 0

    #I prefer to check for the events rather than using key.get_pressed()
    #with key.get_pressed lose precision on the order of key activations
    def input(self, event, indicator, index):  #keyboard input
        self.animation_idx = index
        if event == None:
            self.apply_input()
            return
        if event.key == K_UP or event.key == K_w:
            self.motion['up'] = indicator
        if event.key == K_DOWN or event.key == K_s:
            self.motion['down'] = indicator
        if event.key == K_RIGHT or event.key == K_d:
            self.motion['right'] = indicator
        if event.key == K_LEFT or event.key == K_a:
            self.motion['left'] = indicator

        if event.key == K_LSHIFT:
            self.motion['run'] = indicator

        self.apply_input()

    def move(self):
        move = self.direction
        if self.direction.magnitude() != 0:
            move = self.direction.normalize()
            self.animation_idx = (self.animation_idx+1)%4

        if self.motion['run']:
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
    counter = 0
    index = 0
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
        self.counter += 1
        for event in pg.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                self.player.input(event, True, self.index)
            elif event.type == KEYUP:
                self.player.input(event, False, self.index)
            else:
                self.player.controller_input(event)
        if self.counter == 30:
            self.counter = 0
            self.index = (self.index+1) % 4
            self.player.input(None, True, self.index)

        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        return True








pg.init()
pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
run = True


front_grandma_spritesheet = SpriteSheet(pg.image.load("../sprites/grandmother/front.png"))
back_grandma_spritesheet = SpriteSheet(pg.image.load("../sprites/grandmother/back.png"))
left_grandma_spritesheet = SpriteSheet(pg.image.load("../sprites/grandmother/left.png"))
right_grandma_spritesheet = SpriteSheet(pg.image.load("../sprites/grandmother/right.png"))

sprite_w, sprite_h = 16, 32
front_granny, back_granny, left_granny, right_granny = [], [], [], []

for i in range(4):
    front_granny.append(front_grandma_spritesheet.get_image(i, sprite_w, sprite_h, 8, (0,0,0)))
    back_granny.append(back_grandma_spritesheet.get_image(i, sprite_w, sprite_h, 8, (0,0,0)))
    left_granny.append(left_grandma_spritesheet.get_image(i, sprite_w, sprite_h, 8, (0,0,0)))
    right_granny.append(right_grandma_spritesheet.get_image(i, sprite_w, sprite_h, 8, (0,0,0)))

level = Level()
level.create_map()

while run:
    screen.fill('black') 

    run = level.run()

    pg.display.update()
    clock.tick(FPS) #Still need to use this to make FPS independent




pg.quit()















