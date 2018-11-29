#Sprite classes for platform game
import pygame as pg
from settings import*
vec = pg.math.Vector2
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allSprites
        #add sprite to these groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game #game info
        self.walking = False
        self.jumping = False
        self.currFrame = 0
        self.lastUpdate = 0 #frame rate of walking animation
        self.loadImages() #load image files
        
        self.image = self.standingImage #standing at start
        self.rect = self.image.get_rect()
        
        scale = 3
        size = self.image.get_size()
        self.w, self.h = size[0], size[1]
            
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0) #vec(xVel, yVel)
        self.acc = vec(0,0) #vec(xAcc, yA)
        self.jumpCount = 0
        self.dir = 1 #facing direction right
            
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
        self.animate() #get next image frame
        
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
        #if not moving
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
            
        self.pos.y += min(15, self.vel.y + 0.5 * self.acc.y)
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
    
    #limit height for short jumps
    def jumpCut(self):
        if self.jumping:
            #limit max upward speed
            if self.vel.y < -5:
                self.vel.y = -5
    
    def jump(self):
        #jump if standing on platform
        self.rect.y += 2
        #check if anyting below player
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2 #undo move
        if hits or self.jumpCount < 2:
            #max 2 consecutive jumps
            self.walking = False
            self.jumping = True
            self.jumpCount += 1
            self.vel.y = -PLAYER_JUMP
            if hits:
                self.jumpCount = 1

    def animate(self):
        now = pg.time.get_ticks()

        #check x velocity
        if self.vel.x != 0:
            self.walking = True
        else: self.walking = False
        #show walk animation
        
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jumpImage
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        elif self.walking:
            #if time margin passed
            if now - self.lastUpdate > 100:
                self.lastUpdate = now
                self.currFrame = (self.currFrame + 1) % len(self.walkingFrames)
                bottom = self.rect.bottom
                self.image = self.walkingFrames[self.currFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #player standing
        elif not self.jumping and not self.walking:
            bottom = self.rect.bottom
            self.image = self.standingImage
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            
    #shoot bullets        
    def shoot(self):
        Bullet(self.game, self.rect.centerx, self.rect.centery, self.dir)
        
                    
#platforms to jump on            
from random import choice, randrange
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.platforms
        #add sprite to these groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [self.game.cloud, self.game.cloud2]
        self.image = choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #likelihood of getting power up
        if randrange(100) < 10:
            #generate power up on platform
            PowerUp(self.game, self)
        elif randrange(100) < 10:
            #generate extra life
            ExtraLife(self.game, self)
  
#powerUp on platform
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.allSprites, game.powerUps
        #add sprite to these groups
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.floatH = 5 #coin float height
        self.game = game
        self.plat = plat
        self.type = "coin" #power up type
        self.image = self.game.coin
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - self.floatH
    
    #update location
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        self.rect.centerx = self.plat.rect.centerx
        #check if platform still exists
        if not self.game.platforms.has(self.plat):
            self.kill() #delete powerup
            
class ExtraLife(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.allSprites, game.powerUps
        pg.sprite.Sprite.__init__(self, self.groups)
    
        self.floatH = 5 #heart float height
        self.game = game
        self.plat = plat
        self.image = self.game.heart
        self.type = "heart"
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - self.floatH
    
    #update location
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        self.rect.centerx = self.plat.rect.centerx
        #check if platform still exists
        if not self.game.platforms.has(self.plat):
            self.kill() #delete powerup'''
        

#enemy sprites to attack player
class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allSprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bee
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT*3/4)
        self.vy = 0
        self.dy = 0.5
        self.lastBullet = 0
    
    #move enemey up and down
    def update(self):
        now = pg.time.get_ticks()
        #fire bullet
        if now - self.lastBullet > 2000 + random.choice([-1000, 
        -500, 0, 500, 1000]):
            self.lastBullet = now
            EnemyBullet(self.game, self.rect.centerx, self.rect.centery, 
            self.vx/abs(self.vx))
        
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.vx >= 0:
            self.image = pg.transform.flip(self.game.bee, True, False)
        else:
            self.image = self.game.bee
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        #moved off of the screen
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        
            
#bullets to attack and fire
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self.groups = game.allSprites, game.bullets
        #add sprite to these groups
        pg.sprite.Sprite.__init__(self, self.groups)
        #bullet attributes
        self.image = pg.Surface((10, 10))
        self.image.fill((200, 200, 0))
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.centery = y
        self.rect.centerx = x
        self.xSpeed = 10 * dir
        
    def update(self):
        self.rect.x += self.xSpeed
        #kill if it moves off the screen
        if self.rect.x < 0 or self.rect.x > self.game.screenW:
            self.kill()
        
#bullets to attack and fire
class EnemyBullet(Bullet):
    def __init__(self, game, x, y, dir):
        self.groups = game.allSprites, game.enemyBullets
        #add sprite to these groups
        pg.sprite.Sprite.__init__(self, self.groups)
        #bullet attributes
        self.image = pg.Surface((10, 10))
        self.image.fill((250, 10, 10))
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.centery = y
        self.rect.centerx = x
        self.xSpeed = 10 * dir


