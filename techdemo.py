import module_manager
module_manager.review()
import pygame

#Game class
class GameRuntime(object):
    def __init__(self):
        pygame.init()
        
        #graphics dimenions: width and height
        self.screenW = 900 
        self.screenH = 600 
        self.charR = 50 #player radius
        self.charW = 15
        self.charH = 24
        
        #player position
        self.x = self.screenW/2
        self.y = self.screenH-self.charR
        self.xVel = 10 #x velocity
        self.yVel = 10 #y velocity
        self.charBox = (self.x-self.charW*self.charR/2, 
            self.y-self.charH*self.charR/2, 
            self.charW, 
            self.charH)
        
        self.platforms = [] #pos of platforms
        
        self.jumpCount = 10 #jump height
        self.isJump = False
        self.isLeft = False
        
        self.groundH = 50 #ground height
        
        self.standing = pygame.image.load('stand.png')
        
        self.jump = pygame.image.load('jump.png')
        
        self.walk = [pygame.image.load('walk_1.png'), 
        self.standing, pygame.image.load('walk_2.png'), self.standing]
        
        self.walkCount = 0

        self.isWalk = False
        self.isJumping = False
        

        
        #gameState
        self.gameover = False
        
        #manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
        #set window width and height [width/2, height/2]
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))

        #loop until the user clicks close button.
        self.done = False
    
    #draw player    
    def drawChar(self):
        '''pygame.draw.circle(self.screen, (200,200,0), (int(self.x), 
            int(self.y) - self.groundH), self.charR)'''
            
        pygame.draw.rect(self.screen, (255,0,0), self.charBox, 2)
        if self.isJump:
            if self.isLeft:
                self.char = pygame.transform.flip(self.jump, True, False)
            else:
                self.char = self.jump
        
        elif self.isWalk:
            self.char = self.walk[self.walkCount % 4]
    
        else:
            self.char = self.standing
            
        self.char = pygame.transform.scale(self.char, 
            (self.charR*2,self.charR*2))
            
        self.screen.blit(self.char, 
        (self.x -self.charR, self.y -self.charR- self.groundH))
    
    #draw graphics
    def redrawAll(self):
        self.screen.fill((0,0,0)) #bg
        
        #draw platforms
        pygame.draw.rect(self.screen, (0,200,0), [200, 400, 150, 10], 2)
        pygame.draw.rect(self.screen, (0,200,0), [500, 500, 150, 10], 2)
        
        
        #draw ground
        pygame.draw.rect(self.screen, (20, 200, 10), 
        [0,self.screenH - self.groundH, self.screenW, self.screenH])
        
        #draw player
        self.drawChar()
                
        #update screen        
        pygame.display.update()
    
    #handle mouse clicks
    def mousePressed(self):
        pass
    
    #handle key presses    
    def keyPressed(self):
        width = self.charR
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] :
            self.isWalk = True
            self.isLeft = True
            self.walkCount += 1
            if self.x - self.charR <= 0: #if touching left wall
                self.x += self.xVel
            self.x -= self.xVel #move left

        elif keys[pygame.K_RIGHT] :
            self.isWalk = True
            self.isLeft = False
            self.walkCount += 1
            if self.x + self.charR >= self.screenW:
                self.x -= self.xVel
            self.x += self.xVel
        else: self.isWalk = False
        
        #space key = player jump 
        if not(self.isJump):
            if keys[pygame.K_UP]:
                self.isJumping = True
                self.isJump = True 
            else:
                self.isJump = False
        else:
            if self.jumpCount >= -self.yVel:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = self.yVel
                
    
                           
    def run(self):
        #MAIN PROGRAM LOOP
        while not self.done:
            if self.gameover:
                font = pygame.font.Font(None, 36)
                text = font.render("Game over!", 1, (0, 0, 0))
                self.screen.blit(text, (100,100))
                break
                
            #check user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #clicked close
                    print("bye!")
                    self.done = True #exit loop
            
            self.keyPressed()
            
            self.redrawAll() #update window graphics
            
            #frames per second
            self.clock.tick(20)
        
        #close window and quit        
        pygame.quit() 

#Run game!
game = GameRuntime()
game.run()
                
                
                
                
                
                
                
                
                
                
                
                
                