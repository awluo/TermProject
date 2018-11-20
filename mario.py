import module_manager
module_manager.review()
import pygame
from player import Player
from platforms import Platform

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
        
        self.groundH = 50 #ground height
        
        #player
        self.cat = Player(self.screenW, self.screenH, self.charW, 
        self.charH, self.groundH)
        
        self.platforms = [Platform(200,400),Platform(700,500)] #pos of platforms

        #gameState
        self.gameover = False
        
        #manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
        #set window width and height [width/2, height/2]
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))

        #loop until the user clicks close button.
        self.done = False
        
        self.myfont = pygame.font.SysFont('arial bold', 40)
        self.textsurface = self.myfont.render("score: "+str(self.score), False, (250, 250, 250))
    
    #draw player    
    def drawChar(self):
        self.cat.drawChar(self.screen)
    
    #draw graphics
    def redrawAll(self):
        self.screen.fill((0,0,0)) #bg
        
        for platform in self.platforms:
            platform.draw(self.screen) #draw all bullets
        
        #draw ground
        pygame.draw.rect(self.screen, (20, 200, 10), 
        [0,self.screenH - self.groundH, self.screenW, self.screenH])
        
        #draw player
        self.cat.drawChar(self.screen)
    

        self.screen.blit(self.textsurface,(10,10))
                
        #update screen        
        pygame.display.update()
    
    #handle mouse clicks
    def mousePressed(self):
        pass
    
    #handle key presses    s
    def keyPressed(self):
        
        width = self.cat.width
        keys = pygame.key.get_pressed()
        
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
        

                
    
                           
    def run(self):
        #MAIN PROGRAM LOOP
        while not self.done:

            while(self.cat.y <= self.groundH - self.cat.height/2):
                self.cat.y += 5
            
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
                
                
                
                
                
                
                
                
                
                
                
                
                