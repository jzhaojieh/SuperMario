import pygame
from pygame.locals import *
import sys
import random 
vec = pygame.math.Vector2

width, height = 800,240
size = (width,height)
x,y = 0, height//2
movex,movey = 0,0
white = (255,255,255)
powerupImage = {'shroom': '/Users/joshuahuang/Desktop/112/TP/TP/shroom.png'}
playerImage = { 0: "/Users/joshuahuang/Desktop/112/TP/charr.png", 
                1: "/Users/joshuahuang/Desktop/112/TP/bcharr.png"}
def quit():
    pygame.quit()
    sys.exit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.state = 0 
        self.image = pygame.image.load(playerImage[self.state])
        self.image = pygame.transform.scale(self.image,(30,30))
        self.rect = self.image.get_rect() 
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.hspeed = 0
        self.vspeed = 0
        self.mask = pygame.mask.from_surface(self.image)

        
    def set_position(self,x,y):
        self.rect.x= x-self.origin_x
        self.rect.y= y-self.origin_y
        
    def change_speed(self, hspeed, vspeed):
        self.hspeed += hspeed
        self.vspeed += vspeed
    
    def gravity(self,gravity = .35):
        if self.vspeed == 0: self.vspeed = 1
        else: self.vspeed += gravity 
        if self.rect.y  >= height-60 and self.vspeed >=0:
            self.vspeed = 0
            self.rect.y = height-60
    def changeState(self, level):
        if level < 0:
            quit()
        else:
            self.image = pygame.image.load(playerImage[self.state])
            self.image = pygame.transform.scale(self.image,(30,30))
        
    def jump(self,collide):
        self.vspeed = -6
        
    def update(self, collidable, curLevel):
        self.gravity()
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        self.mask = pygame.mask.from_surface(self.image)

    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/goomba.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect()
        self.hspeed = 0
        self.rect.x = x
        self.rect.y = y

    def update(self, collide, speed = -1):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        #if len(pygame.sprite.spritecollide(self, collide, False)) > 0:
        #    speed *= -1
        global count
        if count == 5:
            self.rect.x += 1
            count = 0
    
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, w = 50, h = 50):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/pipe.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.rect.y = y
        self.rect.x = x
        
    def set_position(self,x,y):
        self.rect.x= x-self.origin_x
        self.rect.y= y-self.origin_y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self,type,x,y,w,h):
        super().__init__()
        self.type = type
        self.image = pygame.image.load(powerupImage[type])
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def update(self, collide, speed = -1):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        #if len(pygame.sprite.spritecollide(self, collide, False)) > 0:
        #    speed *= -1
        global count
        if count == 5:
            self.rect.x += 1
            count = 0
        
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/brick.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)
        
class Block2(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/block.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class QBlock(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/qblock.jpg")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

                
class Level():
    world_shift = 0
    
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
    
    def update(self):
        self.platforms.update()
        self.enemies.update()
    
    def draw(self, screen):
        self.platforms.draw(screen)
        self.enemies.draw(screen)
    
    def shift_world(self, shift):
        self.world_shift += shift
        for platforms in self.collide:
            platforms.rect.x += shift
    
    def startScreen(self):
        surface = font.render("Press a key to start",True)
        rect = surface.get_rect()
        rect.midtop = (width//2, height//2)
        self.screen.blit(surface, rect.midtop)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pg.KEYUP:
                    break
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.collide = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.qbs = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()
        qb1 = QBlock(300,height-105, 18,18)
        qb2 = QBlock(381,height-105, 18,18)
        qb3 = QBlock(417,height-105, 18,18)
        qb4 = QBlock(399,height-180, 18,18)
        qb5 = QBlock(1193,height-105, 18,18)
        qb6 = QBlock(1445,height-170, 18,18)
        qb7 = QBlock(1780,height-105, 18,18)
        qb8 = QBlock(1834,height-105, 18,18)
        qb9 = QBlock(1834,height-170, 18,18)
        qb10 = QBlock(1888,height-105, 18,18)
        qb11 = QBlock(2284,height-170, 18,18)
        qb12 = QBlock(2302,height-170, 18,18)
        qb13 = QBlock(2711,height-105, 18,18)
        b1 = Block(363,height-105,18,18)
        b2 = Block(399,height-105,18,18)
        b3 = Block(435,height-105,18,18)
        b4 = Block(1175,height-105, 18,18)
        b5 = Block(1211,height-105, 18,18)
        b6 = Block(1229,height-170,18,18)
        b7 = Block(1247,height-170,18,18)
        b8 = Block(1265,height-170,18,18)
        b9 = Block(1283,height-170,18,18)
        b10 = Block(1301,height-170,18,18)
        b11 = Block(1319,height-170,18,18)
        b12 = Block(1337,height-170,18,18)
        b13 = Block(1355,height-170,18,18)
        b14 = Block(1391,height-170,18,18)
        b15 = Block(1409,height-170,18,18)
        b16 = Block(1427,height-170,18,18)
        b17 = Block(1445,height-105,18,18)
        b18 = Block(1600,height-105,18,18)
        b19 = Block(1618,height-105,18,18)
        b20 = Block(2050,height-105,18,18)
        b21 = Block(2140,height-170,18,18)
        b22 = Block(2122,height-170,18,18)
        b23 = Block(2158,height-170,18,18)
        b24 = Block(2266,height-170,18,18)
        b26 = Block(2284,height-105, 18,18)
        b27 = Block(2302,height-105, 18,18)
        b25 = Block(2320,height-170,18,18)
        b28 = Block(2675,height-105, 18,18)
        b29 = Block(2693,height-105, 18,18)
        b30 = Block(2729,height-105, 18,18)
        g1 = Enemy(600,height-60)
        pipe1 = Pipe(550,height-60, 35, 30)
        pipe2 = Pipe(750,height-80, 35, 50)
        pipe3 = Pipe(950,height-105, 35, 75)
        pipe4 = Pipe(2600,height-60, 35, 30)
        pipe5 = Pipe(2840,height-60, 35, 30)
        lvl1 = "/Users/joshuahuang/Desktop/112/TP/1-1.png"
        self.mario = Player()
        self.mario.set_position(20,height)
        self.background = pygame.image.load(lvl1).convert()
        self.collide.add(g1,qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,pipe1,pipe2,pipe3,pipe4,pipe5)
        self.blocks.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30)
        self.qbs.add(qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13)
        self.pipes.add(pipe1,pipe2,pipe3,pipe4,pipe5)
        self.players.add(self.mario)
        self.enemies.add(g1)
        self.allsprites.add(self.mario,g1,qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,pipe1,pipe2,pipe3,pipe4,pipe5)
        self.level_limit = -2700
    

if (__name__ == "__main__"):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Mario")
    levelnum = 0
    levels = [Level1()]
    curLevel = levels[levelnum]
    running = True
    clock = pygame.time.Clock()
    count =0 
    
    while running:
        count += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    quit()
                if event.key == K_w:
                    if curLevel.mario.vspeed == 0:
                        curLevel.mario.jump(curLevel.collide)
                if event.key == K_s:
                    pass
                if event.key == K_a:
                    curLevel.mario.change_speed(-2,0)
                if event.key == K_d:
                    curLevel.mario.change_speed(2,0)
            elif event.type == KEYUP:
                if event.key == K_w:
                    if curLevel.mario.vspeed != 0: curLevel.mario.vspeed = 0
                if event.key == K_a:
                    if curLevel.mario.hspeed != 0: curLevel.mario.hspeed = 0
                if event.key == K_d:
                    if curLevel.mario.hspeed != 0: curLevel.mario.hspeed = 0
        #side scrolling from http://programarcadegames.com/python_examples/show_file.php?file=platform_scroller.py
        if curLevel.mario.rect.right >= 500:
            diff = curLevel.mario.rect.right - 500
            curLevel.mario.rect.right = 500
            curLevel.shift_world(-diff)
        if curLevel.mario.rect.left <= 120:
            diff = 120 - curLevel.mario.rect.left
            curLevel.mario.rect.left = 120
            curLevel.shift_world(diff)
        if curLevel.world_shift <= curLevel.level_limit:
            levelnum += 1
            curLevel = levels[levelnum]
            
        enemies = pygame.sprite.spritecollide(curLevel.mario, curLevel.enemies, True)
        for enemy in enemies:
            if curLevel.mario.rect.y < enemy.rect.y:
                curLevel.allsprites.remove(enemy)
                curLevel.collide.remove(enemy)
            else:
                curLevel.mario.state -= 1
                curLevel.mario.changeState(curLevel.mario.state)
                
        poweruphits = pygame.sprite.spritecollide(curLevel.mario, curLevel.powerups, False)
        for hit in poweruphits:
            if hit.type == 'shroom':
                if curLevel.mario.state == 0:
                    curLevel.mario.state += 1
                    curLevel.mario.changeState(curLevel.mario.state)
                    curLevel.allsprites.remove(hit)
                    curLevel.collide.remove(hit)
                    
            
        curLevel.mario.rect.x += curLevel.mario.hspeed
        curLevel.mario.rect.y += curLevel.mario.vspeed
        collision_list = pygame.sprite.spritecollide(curLevel.mario, curLevel.blocks, False)
        for collided_object in collision_list:
            if curLevel.mario.hspeed > 0:
                curLevel.mario.rect.right = collided_object.rect.left
                curLevel.mario.hspeed = 0
            elif curLevel.mario.hspeed < 0:
                curLevel.mario.rect.left = collided_object.rect.right
                curLevel.mario.hspeed = 0
        curLevel.mario.rect.y += curLevel.mario.vspeed
        collision_list = pygame.sprite.spritecollide(curLevel.mario, curLevel.collide, False)
        for collided_object in collision_list:
            if curLevel.mario.vspeed > 0:
                curLevel.mario.rect.bottom = collided_object.rect.top
                curLevel.mario.vspeed = 0
            elif curLevel.mario.vspeed < 0:
                curLevel.mario.rect.top = collided_object.rect.bottom
                curLevel.mario.vspeed = 0
                

        curLevel.allsprites.update(curLevel.collide,levels[levelnum])
        screen.blit(curLevel.background, (curLevel.world_shift,2))
        curLevel.allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(240)