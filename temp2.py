#music from https://archive.org/details/SuperMarioBros.ThemeMusic, http://www.bfxr.net/

import pygame
from pygame.locals import *
import sys
import random 
import time 

width, height = 800,240
size = (width,height)
x,y = 0, height//2
movex,movey = 0,0
white = (255,255,255)
black = (0,0,0)

koopaImage= {2:"/Users/joshuahuang/Desktop/112/TP/flying.png",
              1:"/Users/joshuahuang/Desktop/112/TP/koopa.png",
              0:"/Users/joshuahuang/Desktop/112/TP/shell.png"}
#levels and koopa images from http://www.mariouniverse.com/sprites/
powerupImage = {'shroom': '/Users/joshuahuang/Desktop/112/TP/TP/shroom.png'}
#mushroom from http://fantendo.wikia.com/wiki/Mystery_Mushroom
walking_frames_r = {0:["/Users/joshuahuang/Desktop/112/TP/walking1.png",
                                 "/Users/joshuahuang/Desktop/112/TP/walking2.png"],
                                 1:["/Users/joshuahuang/Desktop/112/TP/walking1b.png",
                                    "/Users/joshuahuang/Desktop/112/TP/walking2b.png"]}
                                    
jump_frame = {0:"/Users/joshuahuang/Desktop/112/TP/jumping.png",
                1: "/Users/joshuahuang/Desktop/112/TP/jumpingb.png"}
#mario frames from https://www.howtogeek.com/howto/44230/what-can-super-mario-teach-us-about-graphics-technology/
fireImage = {0: '/Users/joshuahuang/Desktop/112/TP/fire/24.png', 1: '/Users/joshuahuang/Desktop/112/TP/fire/25.png', 2: '/Users/joshuahuang/Desktop/112/TP/fire/26.png', 3: '/Users/joshuahuang/Desktop/112/TP/fire/27.png', 4: '/Users/joshuahuang/Desktop/112/TP/fire/28.png', 5: '/Users/joshuahuang/Desktop/112/TP/fire/29.png', 6: '/Users/joshuahuang/Desktop/112/TP/fire/30.png', 7: '/Users/joshuahuang/Desktop/112/TP/fire/31.png', 8: '/Users/joshuahuang/Desktop/112/TP/fire/32.png', 9: '/Users/joshuahuang/Desktop/112/TP/fire/33.png', 10: '/Users/joshuahuang/Desktop/112/TP/fire/34.png', 11: '/Users/joshuahuang/Desktop/112/TP/fire/35.png', 12: '/Users/joshuahuang/Desktop/112/TP/fire/36.png', 13: '/Users/joshuahuang/Desktop/112/TP/fire/37.png', 14: '/Users/joshuahuang/Desktop/112/TP/fire/38.png', 15: '/Users/joshuahuang/Desktop/112/TP/fire/39.png', 16: '/Users/joshuahuang/Desktop/112/TP/fire/40.png', 17: '/Users/joshuahuang/Desktop/112/TP/fire/41.png', 18: '/Users/joshuahuang/Desktop/112/TP/fire/42.png', 19: '/Users/joshuahuang/Desktop/112/TP/fire/43.png', 20: '/Users/joshuahuang/Desktop/112/TP/fire/44.png', 21: '/Users/joshuahuang/Desktop/112/TP/fire/45.png', 22: '/Users/joshuahuang/Desktop/112/TP/fire/46.png', 23: '/Users/joshuahuang/Desktop/112/TP/fire/47.png', 24: '/Users/joshuahuang/Desktop/112/TP/fire/48.png', 25: '/Users/joshuahuang/Desktop/112/TP/fire/49.png', 26: '/Users/joshuahuang/Desktop/112/TP/fire/50.png', 27: '/Users/joshuahuang/Desktop/112/TP/fire/51.png', 28: '/Users/joshuahuang/Desktop/112/TP/fire/52.png', 29: '/Users/joshuahuang/Desktop/112/TP/fire/53.png',30: '/Users/joshuahuang/Desktop/112/TP/fire/52.png', 31:'/Users/joshuahuang/Desktop/112/TP/fire/51.png',32:'/Users/joshuahuang/Desktop/112/TP/fire/50.png',33: '/Users/joshuahuang/Desktop/112/TP/fire/49.png',34: '/Users/joshuahuang/Desktop/112/TP/fire/48.png',35: '/Users/joshuahuang/Desktop/112/TP/fire/47.png',36: '/Users/joshuahuang/Desktop/112/TP/fire/46.png',37: '/Users/joshuahuang/Desktop/112/TP/fire/45.png',38: '/Users/joshuahuang/Desktop/112/TP/fire/44.png',39: '/Users/joshuahuang/Desktop/112/TP/fire/43.png',40: '/Users/joshuahuang/Desktop/112/TP/fire/42.png',}
# fire bar from https://www.mariowiki.com/Fire_Bar

def quit():
    #ends the game
    pygame.quit()
    sys.exit()

def gameOver():
    #ends music 
    pygame.mixer.music.fadeout(500)
    gameOver = True
    #displays game over screen
    while gameOver:
        screen.fill(black)
        text = pygame.font.SysFont("monospace",24)
        label = text.render("Game Over!", 1, (255,255,0))
        screen.blit(label,(width//2-100,100))
        label2 = text.render("Press any key to quit", 1, (255,255,0))
        screen.blit(label2,(width//2-100,150))
        pygame.display.flip()
        #ends when key is pressed 
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                quit()

def winScreen():
    #displays winning screen
    won = True
    while won:
        text = pygame.font.SysFont("monospace",24)
        label = text.render("You Win!", 1, (255,255,255))
        label2 = text.render("Press any key to quit", 1, (255,255,255))
        screen.fill(black)
        image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/end.png")
        image = pygame.transform.scale(image, (width,height))
        screen.blit(image, (0,0))
        screen.blit(label,(width//2-50,150))
        screen.blit(label2,(width//2-100,200))
        pygame.display.flip()
        for event in pygame.event.get():
            #ends when key is pressed 
            if event.type == KEYDOWN:
                won = False
                quit()
                    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.state = 0 
        self.current_frame = 0
        self.image = pygame.image.load(walking_frames_r[self.state][self.current_frame])
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect() 
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.hspeed = 0
        self.vspeed = 0
        self.lives = 3
        self.walking = False
        self.jumping = False
        self.colliding = False
        self.last_update = 0
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_position(self,x,y):
        #moves player to position 
        self.rect.x= x-self.origin_x
        self.rect.y= y-self.origin_y
        
    def change_speed(self, hspeed, vspeed):
        #adds horizontal/vertical speed
        self.hspeed += hspeed
        self.vspeed += vspeed
    
    def gravity(self,gravity = .35):
        #brings player down after jumping
        if self.vspeed == 0: self.vspeed = 1
        else: self.vspeed += gravity 
        #makes sure player doesnt fall past height-60
        if self.rect.y  >= height-60 and self.vspeed >=0:
            self.vspeed = 0
            self.rect.y = height-60
            
    def changeState(self, level):
        #changes image of player if he hits enemy 
        if self.state < 0:
            gameOver()
        if level < 0:
            pass
        else:
            self.image = pygame.image.load(walking_frames_r[self.state][self.current_frame])
            self.image = pygame.transform.scale(self.image,(25,25))
            self.image.set_colorkey(white)
        
    def jump(self):
        if not self.jumping and self.vspeed == 0:
            #makes sure player cannot jump in the air 
            curLevel.jump_sound.play()
            self.jumping = True
            self.vspeed = -8

    def animate(self):
        now = pygame.time.get_ticks()
        if self.hspeed != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                #if player is walking and has not been updated for 200 ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 2
                #determine direction he is facing and choose image 
                if self.hspeed > 0:
                    self.image = pygame.image.load(walking_frames_r[self.state][self.current_frame])
                    self.image = pygame.transform.scale(self.image,(25,25))
                    self.image.set_colorkey(white)
                else:
                    self.image = pygame.image.load(walking_frames_r[self.state][self.current_frame])
                    self.image = pygame.transform.flip(self.image,True,False)
                    self.image = pygame.transform.scale(self.image,(25,25))
                    self.image.set_colorkey(white)
        if self.jumping: #same for jumping
            if self.hspeed >= 0:
                self.image = pygame.image.load(jump_frame[self.state])
                self.image = pygame.transform.scale(self.image,(25,25))
                self.image.set_colorkey(white)
            else:
                self.image = pygame.image.load(jump_frame[self.state])
                self.image = pygame.transform.scale(self.image,(25,25))
                self.image.set_colorkey(white)
                self.image = pygame.transform.flip(self.image,True,False)

    def update(self, collidable=pygame.sprite.Group()):
        self.animate()
        self.gravity()
        collision_list = pygame.sprite.spritecollide(self, collidable, False,pygame.sprite.collide_rect)
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        #checks for collision with objets 
        for collided_object in collision_list:
            if self.hspeed > 0:
                self.rect.right = collided_object.rect.left
                self.hspeed = 0
            elif self.hspeed < 0:
                self.rect.left = collided_object.rect.right
                self.hspeed = 0
        collision_list = pygame.sprite.spritecollide(self, collidable, False,pygame.sprite.collide_rect)
        for collided_object in collision_list:
            if self.vspeed > 0:
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif self.vspeed < 0:
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/goomba.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect()
        self.state = 0
        self.hspeed = 0
        self.rect.x = x
        self.rect.y = y
        self.collide = False
        self.speed = -1

    def update(self, collide, shift):
        if pygame.sprite.spritecollide(self,collide,False): self.speed *= -1
        #if enemy collides with object, move other direction 
        self.rect.x += self.speed
        self.mask = pygame.mask.from_surface(self.image)

class Koopa(pygame.sprite.Sprite):
    def __init__(self, x, y,state):
        super().__init__()
        self.state = state
        self.image = pygame.image.load(koopaImage[self.state])
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.hspeed = 0
        self.rect.x = x
        self.rect.y = y
        self.speed = -1
        self.collide = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, collide, shift):
        #changes image based on state 
        if self.state < 0: pass 
        else:
            self.image = pygame.image.load(koopaImage[self.state])
            self.image = pygame.transform.scale(self.image,(25,25))
            self.image.set_colorkey(white)
        if pygame.sprite.spritecollide(self,collide,False): self.speed *= -1
        if self.speed < 0: self.image = pygame.transform.flip(self.image,True,False)
        if self.state != 2:
            #if enemy not flying, bring him to the ground
            if self.rect.y<= height-60:
                self.rect.y = height-60
        self.rect.x += self.speed

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/lava.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
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
        
class PowerUp(pygame.sprite.Sprite):
    def __init__(self,type,x,y,w,h):
        super().__init__()
        self.type = type
        self.image = pygame.image.load(powerupImage[type])
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

            
class MovingPlatform(pygame.sprite.Sprite):   
    def __init__(self,x,y,w,h,yspeed,boundTop,boundBot,player):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/platform.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.boundTop = boundTop
        self.boundBot = boundBot
        self.yspeed = yspeed
        self.player = player
    
    def update(self):
        self.rect.y += self.yspeed
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            #keeps player on platform 
            if self.yspeed < 0: 
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
        #changes the direction the platform is moving when it hits bound 
        if self.rect.bottom > self.boundBot or self.rect.top < self.boundTop:
            self.yspeed *= -1
            
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/brick.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
class Block2(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/block.png")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Block3(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/b3.png")
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
        self.hit = False

class DBlock(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/TP/qblock.jpg")
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.hit = False

class FBlock(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.current_frame = 0
        self.image = pygame.image.load(fireImage[self.current_frame])
        self.image = pygame.transform.scale(self.image,(35,40))
        self.image.set_colorkey(black)
        self.w = w
        self.h = h
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.last_update = 0
        self.current_frame = 0
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            #same as player animation, but keeps center the same
            cent = self.image.get_rect().center
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 34
            self.image = pygame.image.load(fireImage[self.current_frame])
            self.image = pygame.transform.scale(self.image,(35,40))
            self.image.set_colorkey(black)
            self.image.get_rect().center = cent

class Level():
    world_shift = 0
    
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        
    def update(self):
        self.enemies.update()
    
    def shift_world(self, shift):
        self.world_shift += shift
        for platforms in self.collide:
            platforms.rect.x += shift
    
    def startScreen(self):
        intro = True    
        while intro:
            image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/intro.jpg")
            image = pygame.transform.scale(image,(width-200,height))
            screen.blit(image, (100,0))
            pygame.display.flip()
            for event in pygame.event.get():
                #keypress starts the game 
                if event.type == KEYDOWN:
                    intro = False

    def scoreScreen(self,score):
        scores = True
        while scores:
            image = pygame.image.load("/Users/joshuahuang/Desktop/112/TP/score.png")
            image = pygame.transform.scale(image,(width-200,height))
            screen.fill(black)
            screen.blit(image, (100,0))
            text = pygame.font.SysFont("monospace",20)
            #displays how long the level took 
            label = text.render("Your time was %d seconds!" %score,1, (255,255,0))
            screen.blit(label,(width//2-100,100))
            pygame.display.flip()
            for event in pygame.event.get():
                #keydown moves onto next level 
                if event.type == KEYDOWN:
                    scores = False
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.collide = pygame.sprite.Group()
        self.ecollide = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.movingplatforms = pygame.sprite.Group()
        self.powerupblocks = pygame.sprite.Group()
        self.koopas = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.qbs = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()
        self.fblocks = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        self.jump_sound = pygame.mixer.Sound("/Users/joshuahuang/Desktop/112/TP/Jump.wav")
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
        g1 = Goomba(500,height-60)
        g2 = Koopa(700,height-60,1)
        g3 = Goomba(1200,height-60)
        g4 = Goomba(1550,height-60)
        g5 = Goomba(1800,height-60)
        g6 = Goomba(2550,height-60)
        g7 = Goomba(2800,height-60)
        pipe1 = Pipe(550,height-60, 35, 30)
        pipe2 = Pipe(750,height-80, 35, 50)
        pipe3 = Pipe(950,height-105, 35, 75)
        pipe4 = Pipe(2600,height-60, 35, 30)
        pipe5 = Pipe(2840,height-60, 35, 30)
        lvl1 = "/Users/joshuahuang/Desktop/112/TP/1-1.png"
        self.mario = Player()
        self.mario.set_position(132,height)
        self.background = pygame.image.load(lvl1).convert()
        self.collide.add(g1,g2,g3,g4,g5,g6,g7,qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,pipe1,pipe2,pipe3,pipe4,pipe5)
        self.ecollide.add(qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,pipe1,pipe2,pipe3,pipe4,pipe5)
        self.blocks.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30)
        self.qbs.add(qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13)
        self.powerupblocks.add(qb2,qb5,qb6,qb13)
        self.pipes.add(pipe1,pipe2,pipe3,pipe4,pipe5)
        self.players.add(self.mario)
        self.enemies.add(g1,g3,g4,g5,g6,g7)
        self.koopas.add(g2)
        self.allsprites.add(self.mario,g1,g2,g3,g4,g5,g6,g7,qb1,qb2,qb3,qb4,qb5,qb6,qb7,qb8,qb9,qb10,qb11,qb12,qb13,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,pipe1,pipe2,pipe3,pipe4,pipe5)
        self.level_limit = -2687
class Level2(Level):
    def __init__(self):
        super().__init__()
        self.jump_sound = pygame.mixer.Sound("/Users/joshuahuang/Desktop/112/TP/Jump.wav")
        lvl2 = "/Users/joshuahuang/Desktop/112/TP/1-22.png"
        self.mario = Player()
        self.background = pygame.image.load(lvl2).convert()
        self.collide = pygame.sprite.Group()
        self.ecollide = pygame.sprite.Group() # enemy collision 
        self.koopas = pygame.sprite.Group()
        self.powerupblocks = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.qbs = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.movingplatforms = pygame.sprite.Group()
        self.fblocks = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        g1 = Goomba(350,height-65)
        k1 = Koopa(550,height-100,2)
        qb1 = QBlock(160,height-95,17,17)
        qb2 = QBlock(177,height-95,17,17)
        qb3 = QBlock(194,height-95,17,17)
        qb4 = QBlock(211,height-95,17,17)
        qb5 = QBlock(228,height-95,17,17)
        b1 = Block2(465,height-111,17,17)
        b2 = Block2(625,height-98,17,17)
        b3 = Block2(625,height-113,17,17)
        b4 = Block2(625,height-128,17,17)
        b5 = Block2(640,height-98,17,17)
        b6 = Block2(655,height-98,17,17)
        b7 = Block2(655,height-113,17,17)
        b8 = Block2(625,height-128,17,17)
        b9 = Block2(655,height-113,17,17)
        b10 = Block2(670,height-128,17,17)
        b11 = Block2(685,height-128,17,17)
        b12 = Block2(655,height-128,17,17)
        b13 = Block2(700,height-128,17,17)
        b14 = Block2(700,height-113,17,17)
        b15 = Block2(700,height-98,17,17)
        b16 = Block2(717,height-98,17,17)
        b17 = Block2(730,height-98,17,17)
        b18 = Block2(730,height-113,17,17)
        b19 = Block2(730,height-128,17,17)
        b20 = Block2(838, height-98,17,17)
        b21 = Block2(853, height-98,17,17)
        b22 = Block2(868, height-98,17,17)
        b23 = Block2(883, height-98,17,17)
        b24 = Block2(868, height-83,17,17)
        b25 = Block2(883, height-83,17,17)
        b26 = Block2(913,height-98,17,17)
        b27 = Block2(928,height-98,17,17)
        b28 = Block2(943,height-98,17,17)
        b29 = Block2(958,height-98,17,17)
        b30 = Block2(973,height-98,17,17)
        b31 = Block2(988,height-98,17,17)
        b32 = Block2(1003,height-98,17,17)
        b34 = Block2(1078,height-98,17,17)
        b35 = Block2(1078,height-113,17,17)
        b36 = Block2(1093,height-98,17,17)
        b37 = Block2(1108,height-98,17,17)
        b38 = Block2(1198,height-98,17,17)
        b39= Block2(1213,height-98,17,17)
        b40= Block2(1228,height-98,17,17)
        b41= Block2(1243,height-98,17,17)
        b42= Block2(1258,height-98,17,17)
        b43= Block2(1400,height-128,17,17)
        b44= Block2(1385,height-128,17,17)
        b45= Block2(1370,height-128,17,17)
        b46= Block2(1355,height-128,17,17)
        b47= Block2(1340,height-128,17,17)
        b48= Block2(1417,height-128,17,17)
        b49= Block2(1952,height-60,17,17)
        b50= Block2(1952,height-45,17,17)
        b51= Block2(1967,height-45,17,17)
        b52= Block2(1967,height-60,17,17)
        b53= Block2(1952,height-73,17,17)
        b54= Block2(1967,height-73,17,17)
        b55= Block2(2400,height-114,17,17)
        b56= Block2(2385,height-114,17,17)
        b57= Block2(2370,height-114,17,17)
        b58= Block2(2355,height-114,17,17)
        b59= Block2(2340,height-114,17,17)
        b60= Block2(2325,height-114,17,17)
        b61= Block2(2557,height-82,17,17)
        b62= Block2(2572,height-82,17,17)
        b63= Block2(2587,height-82,17,17)
        b64= Block2(2602,height-82,17,17)
        b65= Block2(2617,height-82,17,17)
        b66= Block2(2632,height-82,17,17)
        b82= Block2(2649,height-82,17,17)
        b83= Block2(2649,height-82,17,17)
        b84= Block2(2666,height-82,17,17)
        b67 = Block2(80,height-213,17,17)
        b68 = Block2(838,height-112,17,17)
        b69 = Block2(838,height-127,17,17)
        b70 = Block2(838,height-142,17,17)
        b71 = Block2(838,height-157,17,17)
        b72 = Block2(838,height-172,17,17)
        b73 = Block2(853,height-112,17,17)
        b74 = Block2(853,height-127,17,17)
        b75 = Block2(853,height-142,17,17)
        b76 = Block2(853,height-157,17,17)
        b77 = Block2(853,height-172,17,17)
        b78 = Block2(1093,height-112,17,17)
        b79 = Block2(1093,height-127,17,17)
        b80 = Block2(1093,height-142,17,17)
        b81 = Block2(1093,height-157,17,17)
        p1 = MovingPlatform(2455,height-110,75,15,1,75,height-50,self.mario)
        p2 = MovingPlatform(2225,height-110,75,15,1,75,height-50,self.mario)
        for i in range(80,2200,15):
            b = Block2(i, height-213,17,17)
            self.collide.add(b)
            self.blocks.add(b)
            self.allsprites.add(b)
        pipe1 = Pipe(1642,height-84,35,50)
        pipe2 = Pipe(1749,height-94,35,62)
        pipe3 = Pipe(1840,height-63,35,30)
        k2 = Koopa(760,height-60,1)
        k3 = Koopa(850,height-60,1)
        k4 = Koopa(2000,height-100,2)
        k5 = Koopa(2300,height-60,1)
        g2 = Goomba(1200,height-60)
        g3 = Goomba(1600,height-60)
        g4 = Goomba(1800,height-60)
        self.movingplatforms.add(p1,p2)
        self.collide.add(qb1,qb2,qb3,qb4,qb5,g1,g2,g3,g4,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,b31,b32,b34,b35,b36,b37,b38,b39,b40,b41,b42,b43,b44,b45,b46,b47,b48,b49,b50,b51,b52,b53,b54,b55,b56,b57,b58,b59,b60,b61,b62,b63,b64,b65,b66,b67,b68,b69,b70,b71,b72,b73,b74,b75,b76,b77,b78,b79,b80,b81,b82,b83,b84,pipe1,pipe2,pipe3,k1,k2,k3,k4,k5,p1,p2)
        self.ecollide.add(qb1,qb2,qb3,qb4,qb5,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,b31,b32,b34,b35,b36,b37,b38,b39,b40,b41,b42,b43,b44,b45,b46,b47,b48,b49,b50,b51,b52,b53,b54,b55,b56,b57,b58,b59,b60,b61,b62,b63,b64,b65,b66,b67,b68,b69,b70,b71,b72,b73,b74,b75,b76,b77,b78,b79,b80,b81,b82,b83,b84,pipe1,pipe2,pipe3,p1,p2)
        self.qbs.add(qb1,qb2,qb3,qb4,qb5)
        self.mario.set_position(132,height-60)
        self.players.add(self.mario)
        self.powerupblocks.add(qb1)
        self.enemies.add(g1,g2,g3,g4)
        self.koopas.add(k1,k2,k3,k4,k5)
        self.blocks.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,b31,b32,b34,b35,b36,b37,b38,b39,b40,b41,b42,b43,b44,b45,b46,b47,b48,b49,b50,b51,b52,b53,b54,b55,b56,b57,b58,b59,b60,b61,b62,b63,b64,b65,b66,b67,b68,b69,b70,b71,b72,b73,b74,b75,b76,b77,b78,b79,b80,b81,b82,b83,b84)
        self.allsprites.add(self.mario,qb1,qb2,qb3,qb4,qb5,g1,g2,g3,g4,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,b31,b32,b34,b35,b36,b37,b38,b39,b40,b41,b42,b43,b44,b45,b46,b47,b48,b49,b50,b51,b52,b53,b54,b55,b56,b57,b58,b59,b60,b61,b62,b63,b64,b65,b66,b67,b68,b69,b70,b71,b72,b73,b74,b75,b76,b77,b78,b79,b80,b81,b82,b83,b84,pipe1,pipe2,pipe3,k1,k2,k3,k4,k5,p1,p2)
        self.pipes.add(pipe1,pipe2,pipe3)
        self.level_limit = -2164    
             
class Level3(Level):
    def __init__(self):
        super().__init__()
        self.jump_sound = pygame.mixer.Sound("/Users/joshuahuang/Desktop/112/TP/Jump.wav")
        lvl3 = "/Users/joshuahuang/Desktop/112/TP/1-3.png"
        self.mario = Player()
        self.background = pygame.image.load(lvl3).convert()
        self.collide = pygame.sprite.Group()
        self.ecollide = pygame.sprite.Group()
        self.fblocks = pygame.sprite.Group()
        self.lavas = pygame.sprite.Group()
        self.koopas = pygame.sprite.Group()
        self.powerupblocks = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.qbs = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.movingplatforms = pygame.sprite.Group()
        l1 = Lava(208,height-36,23,40)
        l2 = Lava(422,height-36,25,40)
        l3 = Lava(530,height-36,23,40)
        l4 = Lava(1927,height-37,35,40)
        qb1 = QBlock(480,height-100,18,18)
        qb2 = QBlock(1240,height-100,18,18)
        g1 = Goomba(725,height-60)
        g2 = Goomba(1280,height-60)
        g3 = Goomba(1400,height-60)
        g4 = Goomba(1440,height-60)
        g5 = Goomba(2100,height-60)
        k1 = Koopa(1200,height-110,2)
        for i in range(1675,1840,25):
            l = Lava(i,height-36,25,40)
            self.lavas.add(l)
            self.collide.add(l)
            self.allsprites.add(l)
        for i in range(0,2000,18):
            b = Block3(i, 57,18,18)
            self.collide.add(b)
            self.blocks.add(b)
            self.allsprites.add(b)
        for i in range(1258,1350,18):
            b = QBlock(i,height-100,18,18)
            self.collide.add(b)
            self.qbs.add(b)
            self.allsprites.add(b)
        pipe1 = Pipe(600,height-65,35,30)
        pipe2 = Pipe(770,height-90,35,55)
        pipe3 = Pipe(1630,height-90,35,55)
        f1 = FBlock(300,height-60,15,50)
        f2 = FBlock(1140,height-60,15,50)
        f3 = FBlock(940,height-60,15,50)
        f4 = FBlock(1040,height-60,15,50)
        p1 = MovingPlatform(1680,height-110,60,15,1,100,height-50,self.mario)
        p2 = MovingPlatform(1770,height-110,60,15,1,100,height-50,self.mario)
        p3 = MovingPlatform(1925,height-110,35,15,1,100,height-50,self.mario)
        self.mario.set_position(132,height-60)
        self.collide.add(f1,f2,f3,f4,k1,p1,p2,p3,l1,l2,l3,l4,qb1,g1,g2,g3,g4,g5,pipe1,pipe2,pipe3)
        self.ecollide.add(pipe1,pipe2,pipe3,f1,f2,f3,f4,p1,p2,l1,l2,l3,l4,qb1)
        self.movingplatforms.add(p1,p2,p3)
        self.lavas.add(l1,l2,l3,l4,)
        self.blocks.add()
        self.qbs.add(qb1,qb2)
        self.powerupblocks.add(qb1,qb2)
        self.players.add(self.mario)
        self.fblocks.add(f1,f2,f3,f4)
        self.enemies.add(g1,g2,g3,g4,g5)
        self.koopas.add(k1)
        self.pipes.add(pipe1,pipe2,pipe3)
        self.allsprites.add(self.mario,k1,f1,f2,f3,f4,p1,p2,p3,l1,l2,l3,l4,qb1,g1,g2,g3,g4,g5,pipe1,pipe2,pipe3,)
        self.level_limit = -1770
        
if (__name__ == "__main__"):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Mario")
    #loads background music 
    pygame.mixer.music.load("/Users/joshuahuang/Desktop/112/TP/SuperMarioBros.ogg")
    levelnum = 0
    levels = [Level1(),Level2(),Level3()]
    curLevel = levels[levelnum]
    running = True
    clock = pygame.time.Clock()
    curLevel.startScreen()
    pygame.mixer.music.play(loops=-1) #loops the music 
    start = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:  #keypress on q ends the game 
                    quit()
                if event.key == K_w: # w,a,d to move/jump
                    curLevel.mario.jump()
                    curLevel.mario.animate()
                    curLevel.mario.jumping = False
                if event.key == K_s:
                    pass
                if event.key == K_a:
                    curLevel.mario.change_speed(-2,0)
                if event.key == K_d:
                    curLevel.mario.change_speed(2,0)
            if event.type == KEYUP: #letting go of the key stops marios movement 
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
            end = time.time()
            score = end - start
            #determines how much time the level took 
            curLevel.scoreScreen(score)
            levelnum += 1
            #if passed the last level, show winning screen 
            if levelnum > len(levels) - 1:
                winScreen()
            curLevel = levels[levelnum] #moves to next leve 
            start = time.time() #resets time 
            
        lavahit = pygame.sprite.spritecollide(curLevel.mario,curLevel.lavas,
                                              False,pygame.sprite.collide_circle)
        #checks if mario was hit by lava 
        if lavahit:
            curLevel.mario.state -= 1
            curLevel.mario.changeState(curLevel.mario.state)
        hit = pygame.sprite.spritecollide(curLevel.mario,curLevel.fblocks,False,
                                           pygame.sprite.collide_rect)
        if hit:
            curLevel.mario.state -= 1
            curLevel.mario.changeState(curLevel.mario.state)
                  
        koops = pygame.sprite.spritecollide(curLevel.mario,curLevel.koopas,
                                            False,pygame.sprite.collide_circle)
        #checks collision with koopas
        for enemy in koops:
            if curLevel.mario.rect.y <= enemy.rect.y:
                if enemy.state >= 0 and not enemy.collide:
                    enemy.collide = True
                    enemy.state -= 1
                    curLevel.mario.vspeed = -2
                    if enemy.state < 0:
                        curLevel.allsprites.remove(enemy)
                        curLevel.collide.remove(enemy)
                    curLevel.koopas.update(curLevel.pipes,curLevel.world_shift)
                    enemy.collide = False
            else:
                if enemy.state == 0:
                    curLevel.mario.vspeed = -2
                    curLevel.allsprites.remove(enemy)
                    curLevel.collide.remove(enemy)
                    curLevel.enemies.remove(enemy)
                else:
                    enemy.state -= 1

        enemies = pygame.sprite.spritecollide(curLevel.mario, curLevel.enemies,
                                            False,pygame.sprite.collide_circle)
        #checks collision with other enemies
        for enemy in enemies:
                if curLevel.mario.rect.y >= enemy.rect.y:
                #if mario is below, subtract 1 from his state 
                    if not enemy.collide:
                        enemy.collide = True
                        curLevel.mario.state -= 1
                        if curLevel.mario.state < 0:
                            curLevel.mario.image = pygame.image.load(
                              "/Users/joshuahuang/Desktop/112/TP/gameover.png")
                            curLevel.mario.image = pygame.transform.scale(
                                                 curLevel.mario.image,(25,25))
                            curLevel.mario.image.set_colorkey(white)
                            curLevel.mario.vspeed = -10
                        curLevel.mario.changeState(curLevel.mario.state)
                enemy.collide = False
                        
        enemies = pygame.sprite.spritecollide(curLevel.mario, curLevel.enemies,
                                        False,pygame.sprite.collide_circle)
        for enemy in enemies:
            if curLevel.mario.rect.y < enemy.rect.y:
            #if mario is above, the enemy gets removed 
                curLevel.mario.vspeed = -2
                curLevel.allsprites.remove(enemy)
                curLevel.collide.remove(enemy)
                curLevel.enemies.remove(enemy)

        poweruphits = pygame.sprite.spritecollide(curLevel.mario,
                      curLevel.powerups,False,pygame.sprite.collide_circle)
        for hit in poweruphits:
            if hit.type == 'shroom':
                #mushroom increases mario's' state by 1
                if curLevel.mario.state == 0:
                    curLevel.mario.state += 1
                    curLevel.mario.changeState(curLevel.mario.state)
                    curLevel.allsprites.remove(hit)
                    curLevel.collide.remove(hit)
                else:
                    curLevel.allsprites.remove(hit)
                    curLevel.collide.remove(hit)

        qbs = pygame.sprite.spritecollide(curLevel.mario, curLevel.qbs,
                                            False,pygame.sprite.collide_circle)
        for hit in qbs:
            #generates mushroom above the question block if its a powerup
            if hit in curLevel.powerupblocks:
                if hit.hit == False and curLevel.mario.rect.y > hit.rect.y:
                    hit.hit = True 
                    p1 = PowerUp("shroom",hit.rect.x,hit.rect.y-18, 18,18)
                    curLevel.collide.add(p1)
                    curLevel.allsprites.add(p1)
                    curLevel.powerups.add(p1)
        
        if curLevel.mario.state >= 1:
            blocks = pygame.sprite.spritecollide(curLevel.mario,curLevel.blocks,
                                           False,pygame.sprite.collide_circle)
            #removes block if mario is below and has state of 1
            for hit in blocks:
                if curLevel.mario.rect.y > hit.rect.y:
                    curLevel.mario.vspeed = 0 
                    curLevel.allsprites.remove(hit)
                    curLevel.collide.remove(hit)
                    curLevel.blocks.remove(hit)
        #updates all sprite groups 
        curLevel.fblocks.update()
        curLevel.enemies.update(curLevel.ecollide,curLevel.world_shift)
        curLevel.koopas.update(curLevel.ecollide,curLevel.world_shift)
        curLevel.mario.update(curLevel.collide)
        curLevel.movingplatforms.update()
        screen.blit(curLevel.background, (curLevel.world_shift,0))
        curLevel.allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(500)
    pygame.mixer.music.fadeout(500)