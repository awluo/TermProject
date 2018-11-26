import pygame as pg
from sprites import *
import random

class Game:
    def __init__(self):
        #initialize game window
        pg.init()
        self.font = pg.font.SysFont('arial bold', 40)
        
        #frames per second
        self.FPS = 60
        
        #graphics dimenions: width and height
        self.screenW = 900 
        self.screenH = 600 
        
        #manage how fast the screen updates
        self.clock = pg.time.Clock()
        
        #set window width and height [width/2, height/2]
        self.screen = pg.display.set_mode((self.screenW, self.screenH))
        
        self.running = True
        self.highScores = [0,0,0,0,0]
        self.platH = 15 #platform height

    
    def new(self):
        #start a new game
        #self.__init__()
        self.ground = Ground(0, HEIGHT-40, WIDTH, 40)
        self.newHighScore = False
        
        #starting platforms (x, y, width, height)
        self.platformList = [ self.ground,
                        Platform(WIDTH/2 - 50, HEIGHT * 3/4, 100, self.platH),
                        Platform(380, 300, 100, self.platH),
                        Platform(675, 100, 100, self.platH),
                        Platform(705, 200, 200, self.platH),
                        Platform(505, 100, 100, self.platH),
                        Platform(805, 129, 200, self.platH),
                        Platform(105, 400, 200, self.platH)]
        self.score = 0
        self.allSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.allSprites.add(self.player)
        self.allSprites.add(self.ground)
        for p in self.platformList:
            self.allSprites.add(p)
            self.platforms.add(p)
        self.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        
    def update(self):
        #Game Loop - Update
        self.allSprites.update()
        #check platform collisions only if fallling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #land on object
                self.player.pos.y = hits[0].rect.top 
                #stop moving downward
                self.player.vel.y = 0
        #check gameOver
        if self.player.rect.bottom >= self.ground.rect.top:
            self.playing = False
        
    def events(self):
        #Game Loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            #space - jump        
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                    
        
        #key presses            
        keys = pg.key.get_pressed()       
        if keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
            #increase score
            self.score += 1
            #move platforms
            for p in self.platforms:
                if not type(p) == Ground:
                    p.rect.x -= self.player.vel.x
                    #don't delete ground
                    if p.rect.right <= 0:
                        p.kill() #delete platforms offscreen
                
        #spawn new platforms
        while len(self.platforms) < 12:
            self.newPlatform()
    
    def newPlatform(self):
        #set random dimensions and loc
        width = random.randrange(50, 150)
        height = 20
        x = random.randrange(WIDTH, WIDTH * 1.5)
        y = random.randrange(100, HEIGHT - self.ground.rect.height - 50)
        p = Platform(x, y, width, self.platH)
        self.platforms.add(p)
        self.allSprites.add(p)
        
    #draw game screen
    def draw(self):
        #Game Loop - draw
        self.screen.fill((0,0,0))
        
        self.allSprites.draw(self.screen)
        self.drawText("Score: " + str(self.score), 
        40, (250,250,250), WIDTH/2, 15)
        pg.display.flip()
        
    def showStartScreen(self):
        #game start screen
        self.screen.fill((0,0,0))
        self.drawText("JUMP CAT", 40, (200,200,200), WIDTH/2, HEIGHT/4)
        self.drawText("Arrows to Move, Space to Shoot", 25, 
        (200,200,200), WIDTH/2, HEIGHT/2)

        self.drawText("[Press a key to play]", 30, 
        WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    
    def showGameOver(self):
        #game over screen
        if not self.running:
            return
        self.getHighScores()
        WHITE = (200,200,200)
        self.screen.fill((0,0,0))
        self.drawText("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawHighScores()
        self.drawText("[Press a key to play again]", 30, WHITE, WIDTH / 2, 
        HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    
    def drawHighScores(self):
        txt = "Score: "
        color = WHITE
        if (self.newHighScore): 
            txt = "New High Score: "  
            color = YELLOW
        self.drawText(txt + str(self.score), 30, color, WIDTH / 2, 
        HEIGHT / 3)
        #draw high scores list
        self.drawText("HIGH SCORES ", 25, WHITE, WIDTH / 2, 
        HEIGHT /2.5)
        yIndex = 0
        for score in self.highScores:
            yIndex += 1
            self.drawText(str(score), 25,
            WHITE, WIDTH / 2, HEIGHT/2.5 + yIndex*30)
    
    #wait for key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False
        
    #draw text on screen
    def drawText(self, text, size, color, x, y):
        font = pg.font.SysFont('arial bold', size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x,y)
        self.screen.blit(textSurface, textRect)
    
    def getHighScores(self):
        rank = -1
        for score in self.highScores:
            rank += 1
            if self.score > score: #set new high score value at rank
                self.highScores.insert(rank, self.score)
                self.highScores.pop()
                self.newHighScore = True
                break
    
    def animate(self):
        now = pg.time.get_ticks()
    
        
#Run game!
g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGameOver()

pg.quit()
                
                