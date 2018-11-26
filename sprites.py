#Sprite classes for platform game
import pygame as pg
from settings import*
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game #game info
        self.walking = False
        self.jumping = False
        self.currFrame = 0
        self.lastUpdate = 0 #frame rate of walking animation
        self.loadImages()
        
        self.image = self.standingImage
        #self.image.fill((200,200,0)) #yellow
        self.rect = self.image.get_rect()
            
        scale = 3
        size = self.image.get_size()
        self.w, self.h = size[0] * scale, size[1] * scale
            
        #self.rect.center = (WIDTH/2, 0)
        self.pos = vec(WIDTH/2, 0)
        self.vel = vec(0,0) #vec(xVel, yVel)
        self.acc = vec(0,0) #vec(xAcc, yA)
        self.jumpCount = 0
        

        '''self.rect = pg.Rect(self.pos.x - self, 
            self.pos.y, self.w, self.h)'''
            
        self.rect.center = (WIDTH/2, 0)
        
    #return scaled image 
    def getImage(self, fileName):
        scale = 3 #scale image size by ratio
        img = pg.image.load(fileName)
        size = img.get_size()
        width, height = size[0] * scale, size[1] * scale
        img = pg.transform.scale(img, (width, height))
        return img
    
    def loadImages(self):
        #load images
        self.standingImage = self.getImage('stand.png')
        self.jumpImage = self.getImage('jump.png')
        self.walkingFrames = [self.getImage('walk_1.png'), 
        self.standingImage, self.getImage('walk_2.png'), 
        self.standingImage]
        self.firingImage = self.getImage('firing.png')

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        #jump if standing on platform
        self.rect.x += 1
        #check if anyting below player
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1 #undo move
        if hits or self.jumpCount < 2:
            #max 2 consecutive jumps

            self.jumpCount += 1
            self.vel.y = -PLAYER_JUMP
            if hits:
                self.jumpCount = 1

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Ground(Platform):
    pass



