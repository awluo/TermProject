
import module_manager
module_manager.review()
import pygame

class Player(object):
    def __init__(self, winW, winH, w, h, groundH):
        self.screenW = winW
        self.screenH = winH
        self.radius = 50 #player radius
        self.width = w
        self.height = h
        self.groundH = groundH
        
        #player position
        self.x = winW/2
        self.y = winH - groundH - self.height/2
        self.xVel = 10 #x velocity
        self.yVel = 10 #y velocity
        self.charBox = (self.x-self.width*self.radius/2, 
            self.y-self.height*self.radius/2, 
            self.width, 
            self.height)
        
        self.jumpCount = 10 #jump height
        self.isJump = False
        self.dir = "Right"
        
        self.standing = pygame.image.load('stand.png')
        self.jump = pygame.image.load('jump.png')
        self.walk = [pygame.image.load('walk_1.png'), 
        self.standing, pygame.image.load('walk_2.png'), self.standing]
        self.onPlatform = False
        
        self.walkCount = 0
        self.isWalk = False
        self.isJumping = False
        
    def drawChar(self, window):
        pygame.draw.rect(window, (255,0,0), 
            (int(self.x)-self.width/2, int(self.y) - self.groundH, 
            self.width ,self.height), 2)
        
        if self.isJump:
            if self.dir == "Left":
                self.char = pygame.transform.flip(self.jump, True, False)
            else: self.char = self.jump
        
        elif self.isWalk: self.char = self.walk[self.walkCount % 4]
    
        else: self.char = self.standing
            
        self.char = pygame.transform.scale(self.char, 
            (self.radius*2,self.radius*2))
            
        window.blit(self.char, 
        (self.x -self.radius, self.y - self.groundH))
        
        
    def moveLeft(self, platforms):
        if self.x - self.width/2 <= 0: #if touching left wall
            self.x += self.xVel
        self.x -= self.xVel #move left
        #check if falling off platform
        if not self.isJump: self.checkFall(platforms)
        
    def moveRight(self, platforms):
        if self.x + self.width/2 >= self.screenW:
            self.x -= self.xVel
        self.x += self.xVel
        #check if falling off platfrom
        if not self.isJump: self.checkFall(platforms)
    
    #move left or right
    def move(self, dir, platforms):
        self.isWalk = True
        self.dir = dir
        self.walkCount += 1
        if dir == "Left": self.moveLeft(platforms)
        else: self.moveRight(platforms)
    
    #cat jump
    def jumpUp(self, platforms):
        print("jump")
        if self.jumpCount >= -self.yVel:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
                
            newY = -(self.jumpCount ** 2) * 0.5 * neg
            #if not colliding with anything
            if not self.collision(platforms, (0,newY)):
                #jump
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                
                self.jumpCount -= 1
                print("jump")
            else:
                print("no jump")
                self.isJump = False
                self.jumpCount = self.yVel
                    
        
        else:
            #stop jumping
            print("stop jumping")
            self.isJump = False
            self.jumpCount = self.yVel
            self.checkFall(platforms)
            print("done")
    
    #see if player should continue falling        
    def checkFall(self, platforms):
        print("check fall")
        fall = True
        #if in midair
        for platform in platforms:
            #if on platform don't fall
            if platform.x - platform.w/2 - self.width/2 < self.x and \
            self.x < platform.x + platform.w/2 + self.width/2 and \
                self.y < platform.y + platform.h/2 + self.height/2:
                fall = False
                print("dont fall")
        #fall if not on any platform
        if (fall): 
            print("fall")
            self.fall()
    
    #fall to ground
    def fall(self):
        self.onPlatform = False
        print("fall")
        while (self.y < self.screenH - self.groundH - self.height/2):
            self.y += 1
        self.land()
        
    def land(self):
        self.y = self.screenH - self.groundH - self.height/2
        
    
    #dir stored as tuple (x dir, y dir)
    def collision(self, platforms, dir):
        newX = self.x + dir[0]
        newY = self.y + dir[1]
        for platform in platforms:
            #if collided with platform
            if platform.x - platform.w/2 - self.width/2 < newX and \
            newX < platform.x + platform.w/2 + self.width/2 and \
            platform.y - platform.h/2 - self.height/2 < newY and \
                newY < platform.y + platform.h/2 + self.height/2 :
            
                #if jumped onto platform
                if self.isJump and self.y < platform.y - platform.h/2 - self.height/2:
                    self.y = platform.y - platform.h/2 - self.height/2
                    self.onPlatform = True
                    print("on platform")

                    
                    
                #if hit below platform
                elif self.isJump and self.y > platform.y + platform.h/2 + self.height/2:
                    self.fall()
                    self.onPlatform = False
                        

                
                return True
        print("collision")
        return False
        
        
        
        
        
        
     