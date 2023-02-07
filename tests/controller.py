import pygame as pg
from pygame.locals import *

class Enemy():
    def __init__(self, x,y,w,h,color):
        self.rect = Rect(x,y,w,h) 
        self.color=color
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

    def move(self, x, y):
        #collision checks? 
        self.rect.move_ip(x, y)






class Player():
    def __init__(self, x, y,w,h, color):
        self.rect = Rect(x,y,w,h)
        self.head = Rect((x+w/2-7), y+h-7,14,14)
        self.head_pos = [(x-5,(y+h/2-7)), ((x+w/2-7),y-5), (x+w-7,(y+h/2-7)), ((x+w/2-7), y+h-7)] #left, top, right, bottom
        self.head_pos = 3 # 0=left, 1=top, 2=right, 3=bottom
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, (0,0,0), self.head)

    def move(self, x, y):
        #should add collision checks
        self.rect.move_ip(x, y)
        self.head.move_ip(x, y)
    
    def rotate(self, x, y):
        if x > 0 and self.head_pos != 2: 
            new_x, new_y = self.rect.midright
            self.head_pos = 2
            self.head = Rect(new_x-7, new_y-7, 14,14) #to lazy to move the rect, so I just create a new one
        if x < 0 and self.head_pos != 0: 
            new_x, new_y = self.rect.midleft      
            self.head_pos = 0
            self.head = Rect(new_x-7, new_y-7, 14,14)
        if y > 0 and self.head_pos != 3:
            new_x, new_y = self.rect.midbottom
            self.head_pos = 3
            self.head = Rect(new_x-7, new_y-7, 14,14)
        if y < 0 and self.head_pos != 1:
            new_x, new_y = self.rect.midtop
            self.head_pos = 1
            self.head = Rect(new_x-7, new_y-7, 14,14)
 
    def jump(self):
        mv_amnt = 70 #to change it easily
        if self.head_pos == 0:
            self.move(-mv_amnt,0)
        if self.head_pos == 1:
            self.move(0,-mv_amnt)
        if self.head_pos == 2:
            self.move(mv_amnt,0)
        if self.head_pos == 3:
            self.move(0,mv_amnt)






pg.init()
pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

screen = pg.display.set_mode((900, 600))
clock = pg.time.Clock()

run = True
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
MOV_AMOUNT = 4


player = Player(10,10,40,40,RED)
enemy = Enemy(300, 250, 40,40,BLUE)

motion = [0,0]
sprint_mult = 1


while run:
    clock.tick(60)
    screen.fill(WHITE)
    player.draw(screen)
    enemy.draw(screen)
    player.move(motion[0] * sprint_mult, motion[1] * sprint_mult)

    pg.display.update()

    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == JOYBUTTONDOWN:
            print(event)
            if event.button == 0:
                player.jump()
                print("You have pressed a")
            if event.button == 1:
                print("You have pressed b")
            if event.button == 2:
                print("You have pressed x")
            if event.button == 3:
                print("You have pressed y")
            if event.button == 5: #R1 => sprint
                sprint_mult = 2
        if event.type == JOYBUTTONUP:
            if event.button == 5: #R1 => stop sprint
                sprint_mult = 1
            #print(event)
        if event.type == JOYAXISMOTION:
            #print(event)
            if event.axis < 2: #left joystick
                motion[event.axis] = event.value * 6
            # event.axis == 2 => left-back trigger
            if event.axis == 3: #right joystick (poorly designed, I know)
                if abs(event.value) > 0.4: #ignore noise
                    player.rotate(event.value, 0)
            if event.axis == 4:
                if abs(event.value) > 0.4: #ignore noise
                    player.rotate(0, event.value)
    

        #if event.type == JOYHATMOTION: #arrow controller keys
            #print(event)


        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                motion[0] -= MOV_AMOUNT
            elif event.key == K_RIGHT:
                motion[0] += MOV_AMOUNT 
            elif event.key == K_DOWN:
                motion[1] += MOV_AMOUNT 
            elif event.key == K_UP:
                motion[1] -= MOV_AMOUNT
        if event.type == KEYUP:
            if event.key == K_LEFT:
                motion[0] += MOV_AMOUNT
            elif event.key == K_RIGHT:
                motion[0] -= MOV_AMOUNT 
            elif event.key == K_DOWN:
                motion[1] -= MOV_AMOUNT 
            elif event.key == K_UP:
                motion[1] += MOV_AMOUNT



pg.quit()




