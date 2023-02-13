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
    walking_speed = 3 
    running_speed = 5
    direction = pg.math.Vector2()
    motion = {"up": False, "right": False, "down": False, "left": False, "run": False}
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group) #adds this sprite to all sprite groups in groups
        self.image = idle_granny
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)
         
        self.collision_sprites = collision_sprites

    def controller_input(self, event):
        if event.type == JOYHATMOTION:
            self.direction.x = event.value[0]
            self.direction.y = -event.value[1]
        elif event.type == JOYBUTTONDOWN:
            if event.button == 5:
                self.motion['run'] = True
        elif event.type == JOYBUTTONUP:
            if event.button == 5:
                self.motion['run'] = False

    def apply_input(self):
        if self.motion['up'] and not self.motion['down']:
            self.direction.y = -1
        elif not self.motion['up'] and self.motion['down']:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.motion['right'] and not self.motion['left']:
            self.direction.x = 1
        elif not self.motion['right'] and self.motion['left']:
            self.direction.x = -1
        else:
            self.direction.x = 0

    #I prefer to check for the events rather than using key.get_pressed()
    #with key.get_pressed lose precision on the order of key activations
    def input(self, event, indicator):  #keyboard input
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
                self.player.input(event, True)
            elif event.type == KEYUP:
                self.player.input(event, False)
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


grandma_spritesheet = SpriteSheet(pg.image.load("../sprites/grandmother/front.png"))
sprite_w, sprite_h = 16, 32 
idle_granny = grandma_spritesheet.get_image(0, sprite_w, sprite_h, 5, (0,0,0))


level = Level()
level.create_map()

while run:
    screen.fill('black') 

    run = level.run()

    pg.display.update()
    clock.tick(FPS)




pg.quit()















