import pygame as pg
from sprites import *
import random

# Pygame Platformer Base Code Citation
# KidsCanCode - Game Development with Pygame video series

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
        self.cloud = pg.image.load('cloud.png') #platform images
        self.cloud2 = pg.image.load('cloud2.png')
        self.coin = pg.image.load('coin.png') #coin image
        self.bee = pg.image.load('bee.png') #enemy image
        self.heart = pg.image.load('heart.png') #heart image
    
    def new(self):
        #start a new game
        self.allSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerUps = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemyBullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.lives = 3
        
        self.newHighScore = False
        #starting platforms
        self.platformList = [
                        Platform(self, WIDTH/2 - 50, HEIGHT * 3/4),
                        Platform(self, 380, 300),
                        Platform(self, 675, 100),
                        Platform(self, 705, 200),
                        Platform(self, 505, 100),
                        Platform(self, 805, 129),
                        Platform(self, 105, 400)]
        self.score = 0
        self.mobTimer = 0
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
        
        #spawn enemy
        now = pg.time.get_ticks()
        if now - self.mobTimer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mobTimer = now
            Enemy(self)
        # hit mobs?
        mobHits = pg.sprite.spritecollide(self.player, self.enemies, True)
        enemyHits = pg.sprite.spritecollide(self.player, self.enemyBullets, True)
        if mobHits or enemyHits:
            self.loseLife()
        
        #check platform collisions only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                #find lowest platform hit
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:
                    #land on object
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0 #stop moving downward
                        self.player.jumping = False
        
        #check if player hits power  up
        self.checkPowerUps()
        self.checkEnemies()
        
        #check gameOver
        if self.player.rect.top >= self.screenH:
            self.playing = False
    
    #check if player collects power up
    def checkPowerUps(self):
        powHits = pg.sprite.spritecollide(self.player, self.powerUps, True)
        for pow in powHits:
            #increase score
            if pow.type == "coin":
                self.score += 10
            elif pow.type == "heart":
                self.lives += 1
                
    #check if player bullets attack enemy            
    def checkEnemies(self):
        #bullets hits
        for bullet in self.bullets:
            enemyHits = pg.sprite.spritecollide(bullet, self.enemies, True)
            for hit in enemyHits:
                self.score += 10

    def loseLife(self):
        self.lives -= 1 #lose a life
        if self.lives == 0: self.playing = False
        
    def events(self):
        #Game Loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            #up arrow key to jump   
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jumpCut()
                    #space to shoot
                if event.key == pg.K_SPACE:
                    self.player.shoot()
        
        #key presses            
        keys = pg.key.get_pressed()       
        if keys[pg.K_RIGHT]:
            self.player.dir = 1
            self.movePlatforms()
        elif  keys[pg.K_LEFT]:
            self.player.dir = -1
            self.movePlatforms()
                
        #spawn new platforms
        while len(self.platforms) < 12:
            self.newPlatform()
    
    #move platforms in opposite direction
    def movePlatforms(self):
        #move platforms
        for p in self.platforms:
            p.rect.x -= self.player.vel.x
            if p.rect.right <= 0:
                p.kill() #delete platforms offscreen
    
    def newPlatform(self):
        #set random dimensions and loc
        width = random.randrange(50, 150)
        height = 20
        x = random.randrange(WIDTH, WIDTH * 1.5)
        y = random.randrange(100, HEIGHT - 50)
        Platform(self, x, y) #spawn new platform
        
    #draw game screen
    def draw(self):
        #Game Loop - draw
        self.screen.fill((50,150,250))
    
        self.allSprites.draw(self.screen)
        #draw player over everything in front
        self.screen.blit(self.player.image, self.player.rect)
        
        #draw hearts
        self.drawLives()
        
        self.drawText("Score: " + str(self.score), 
        40, (250,250,250), WIDTH/2, 15)
        pg.display.flip()
    
    #draw player lives
    def drawLives(self):
        margin = 60
        height = 20
        for i in range(1, self.lives + 1):
            self.screen.blit(self.heart, (self.screenW - margin*i - 20, height))
        
    def showStartScreen(self):
        #game start screen
        self.screen.fill((0,0,0))
        self.drawText("JUMP CAT", 50, (200,200,0), WIDTH/2, HEIGHT/4)
        self.drawText("Arrows to Move, Space to Shoot", 30, 
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
        self.screen.fill((0,0,0))
        self.drawText("GAME OVER", 48, (250, 10, 0), WIDTH / 2, HEIGHT / 4)
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
    
    #update list of high scores
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
                
                