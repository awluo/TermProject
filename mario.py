##### --- CAT JUMP --- #####
#Amy Luo

import module_manager
module_manager.review()
import pygame
import random
from player import Player
from platforms import Platform
from bullets import Bullet
from enemies import Enemy
import math

#Game class
class GameRuntime(object):
    def __init__(self):
        pygame.init()
        
        #graphics dimenions: width and height
        self.screenW = 900 
        self.screenH = 600 
        self.charR = 50 #image radius
        self.charW = 50 #15 * 3.5
        self.charH = 100 #25 * 4
        self.score = 0
        self.lastBulletTime = 0
        
        self.groundH = 50 #ground height
        
        #player
        self.cat = Player(self.screenW, self.screenH, self.charW, 
        self.charH, self.groundH)
        
        #positions of platforms
        self.platforms = [Platform(200,400),Platform(700,500), 
        Platform(500, 350)] 
        
        self.enemies = [Enemy(200,300), Enemy(400,200)] #list of enemies
        self.bullets = [] #list of bullets

        #gameState
        self.gameover = False
        
        #manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
        #set window width and height [width/2, height/2]
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))

        #loop until the user clicks close button.
        self.done = False
        
        self.myfont = pygame.font.SysFont('arial bold', 40)
    
    #draw player    
    def drawChar(self):
        self.cat.drawChar(self.screen)
    
    #draw graphics
    def redrawAll(self):
        self.screen.fill((0,0,0)) #bg
        
        for platform in self.platforms:
            platform.draw(self.screen) #draw all platforms
        
        #draw ground
        pygame.draw.rect(self.screen, (20, 200, 10), 
        [0,self.screenH - self.groundH, self.screenW, self.screenH])
        
        #draw player
        self.cat.drawChar(self.screen)
        
        #draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
    
        #draw score
        self.textsurface = self.myfont.render("score: "+str(self.score), 
        False, (250, 250, 250))
        self.screen.blit(self.textsurface,(10,10))
                
        #update screen        
        pygame.display.update()
    
    #handle mouse clicks
    def mousePressed(self):
        pass
    
    #handle key presses
    def keyPressed(self):
        keys = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks() #milliseconds
        #space key - fire bullets
        if keys[pygame.K_SPACE] and \
        int(currentTime) - int(self.lastBulletTime) >= 250:
            #fire bullets every half a second 
            self.cat.isFiring = True
            vel = -1
            if self.cat.dir == "Right": vel = 1
            self.bullets.append(Bullet(self.cat.x, self.cat.y - 
            self.cat.h/4, vel))
            self.lastBulletTime = currentTime
        
        #move left and right
        if keys[pygame.K_LEFT] :
            if not self.cat.collision(self.platforms, (-1,0)):
                self.cat.move("Left", self.platforms)
        elif keys[pygame.K_RIGHT] :
            if not self.cat.collision(self.platforms, (1,0)):
                self.cat.move("Right", self.platforms)
        else: self.cat.isWalk = False
        
        #up key = player jump 
        if not(self.cat.isJump):
            if keys[pygame.K_UP]:
                self.cat.isJumping = True
                self.cat.isJump = True 
            else:
                self.cat.isJump = False
        else:
            self.cat.jumpUp(self.platforms)
    
    def getDistance(self, x1, y1, x2, y2):
        distance =  math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    #move bullets forward
    def moveBullets(self):
        for bullet in self.bullets:
            bullet.move()
            #delete if off screen
            if bullet.x - bullet.r < 0 or \
            bullet.x + bullet.r > self.screenW:
                self.bullets.remove(bullet)
            #delete if hitting enemy
            for enemy in self.enemies:
                if self.getDistance(bullet.x, bullet.y, enemy.x, enemy.y) <= \
                bullet.r + enemy.r:
                    enemy.color = (200, 50 ,0) #enemy changes color
                    enemy.getHit() #hit enemey
                    self.bullets.remove(bullet) #remove bullet
                    self.score += 1 #increase score
                    if enemy.hp <= 0: self.enemies.remove(enemy)

    def run(self):
        #MAIN PROGRAM LOOP
        while not self.done:
            
            #check if gameOver state
            if self.gameover:
                font = pygame.font.Font(None, 36)
                text = font.render("Game over!", 1, (0, 0, 0))
                self.screen.blit(text, (100,100))
                break
            
            #move bullets
            self.moveBullets()
                    
            #check user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #clicked close
                    print("bye!")
                    self.done = True #exit loop
            
            self.keyPressed() #check key presses
            
            self.redrawAll() #update window graphics
            
            #frames per second
            self.clock.tick(20)
        
        #close window and quit        
        pygame.quit() 

#Run game!
game = GameRuntime()
game.run()
                
                
                
                
                
                
                
                
                
                
                
                
                