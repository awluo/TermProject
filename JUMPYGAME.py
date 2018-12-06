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
        
        #frames per sec
        self.FPS = 60
        self.maxDist = 1000
        
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
        self.darkCloud = pg.image.load('darkCloud.png')
        self.coin = pg.image.load('coin.png') #coin image
        self.bee = pg.image.load('bee.png') #enemy image
        self.heart = pg.image.load('heart.png') #heart image
        self.rainDrop = pg.image.load('rainDrop.png')
        self.singlePlayer = True
    
    def new(self, playerMode = True):
        #start a new game
        self.allSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerUps = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemyBullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.players = pg.sprite.Group()
        #self.player = Player(self)
        self.lives1 = 3
        self.lives2 = 0
        self.level = 1
        self.distance = 0
        self.mode = "start"
        self.singlePlayer = playerMode
        
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
            if self.mode == "game":
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.drawGame()
            elif self.mode == "start":
                self.showStartScreen()
            elif self.mode == "instructions":
                self.showInstructions()
            elif self.mode == "settings":
                self.showSettings()
        
    def update(self):
        #Game Loop - Update
        self.allSprites.update()
        
        #spawn enemy
        now = pg.time.get_ticks()
        if now - self.mobTimer > 10000 - self.level/2*1000 + \
        random.choice([-1000, -500, 0, 500, 1000]):
            self.mobTimer = now
            Enemy(self)

        
        #check platform collisions only if falling
        for player in self.players:
            self.checkPlatCollide(player)
            
            #check if player hits power  up
            self.checkPowerUps(player)
            #check if player hits enemy/enemy bullet
            self.checkEnemyCollide(player)
            
        self.checkEnemiesKilled()
        
        #check gameOver
        #for player in self.players:
        if self.player.rect.top >= self.screenH:
            self.playing = False
    
    def checkEnemyCollide(self, player):
        #check collision with enemies/enemy bullets
        mobHits = pg.sprite.spritecollide(player, self.enemies, True)
        enemyHits = pg.sprite.spritecollide(player, self.enemyBullets, True)
        if mobHits or enemyHits:
            self.loseLife(player) #lose a life
    
    #check if player collects power up
    def checkPowerUps(self, player):
        powHits = pg.sprite.spritecollide(player, self.powerUps, True)
        for pow in powHits:
            #increase score
            if pow.type == "coin":
                self.score += 10
            elif pow.type == "heart":
                if player.PID == "p1":
                    self.lives1 += 1
                elif player.PID == "p2":
                    self.lives2 += 1
                
    #check if player bullets attack enemy            
    def checkEnemiesKilled(self):
        #bullets hits
        for bullet in self.bullets:
            enemyHits = pg.sprite.spritecollide(bullet, self.enemies, True)
            for hit in enemyHits:
                self.score += 10

    #check platform collision if player is falling
    def checkPlatCollide(self, player):
        self.checkPlatCollideHelper(self.player)
        if not self.singlePlayer:
            self.checkPlatCollideHelper(self.player2)
    
    def checkPlatCollideHelper(self, player):   
        if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if hits:
                lowest = hits[0]
                #find lowest platform hit
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                    if hit.type == "dark":
                        #hit.kill() #delete dark cloud
                        hit.jumpedOn = True
                        hit.jumpTime = pg.time.get_ticks()
                if player.pos.x < lowest.rect.right + 10 and \
                    player.pos.x > lowest.rect.left - 10:
                    #land on object
                    if player.pos.y < lowest.rect.centery:
                        player.pos.y = lowest.rect.top
                        player.vel.y = 0 #stop moving downward
                        player.jumping = False

    #lose a life
    def loseLife(self, player):
        if player.PID == "p1":
            self.lives1 -= 1 
        elif player.PID =="p2":
            self.lives2 -= 1
        if self.lives1 == 0 or \
            (not self.singlePlayer and self.lives2 == 0): self.playing = False
        
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
                elif not self.singlePlayer and event.key == pg.K_w:
                    self.player2.jump()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jumpCut()
                    #space to shoot
                elif not self.singlePlayer and event.key == pg.K_w:
                    self.player2.jumpCut()
                if event.key == pg.K_SPACE:
                    self.player.shoot()
                elif not self.singlePlayer and event.key == pg.K_LCTRL:
                    self.player2.shoot()
                
        
        #key presses            
        keys = pg.key.get_pressed()       
        if keys[pg.K_RIGHT]:
            self.player.dir = 1
            self.updateDistance()
        elif  keys[pg.K_LEFT]:
            self.player.dir = -1
            self.updateDistance()
        if not self.singlePlayer:
            if keys[pg.K_d]:
                self.player2.dir = 1
            elif  keys[pg.K_a]:
                self.player2.dir = -1
                
        #spawn new platforms
        while len(self.platforms) < 12:
            self.newPlatform()
    
    #update player distance, move platforms, check level up
    def updateDistance(self):
        #move platforms
        self.movePlatforms()
        #increase distance
        self.distance += int(self.player.vel.x)
        #check level up
        if self.distance >= self.maxDist:
            self.updateLevel()
            self.distance = 0 #reset to new level
            
    #go to next level
    def updateLevel(self):
        self.level += 1
    
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
    def drawGame(self):
        #Game Loop - draw
        self.screen.fill((50,150,250))
    
        self.allSprites.draw(self.screen)
        #draw player over everything in front
        self.screen.blit(self.player.image, self.player.rect)
        
        if not self.singlePlayer:
            self.drawText("p1", 25, 
            RED, self.player.rect.midtop[0], self.player.rect.midtop[1] - 30)
            self.drawText("p2", 25, 
            BLUE, self.player2.rect.midtop[0], self.player2.rect.midtop[1] - 30)
            
        
        #draw hearts
        self.drawLives()
        
        self.drawText("Score: " + str(self.score), 
        40, (250,250,250), WIDTH/2, 15)
        
        self.drawText("Level: " + str(self.level), 
        40, (250,250,0), 80, 15)
        
        self.drawText("Dist: " + str(self.distance), 
        40, (250,250,0), 80, 50)
        
        pg.display.flip()
    
    #draw player lives
    def drawLives(self):
        margin = 50
        height = 10
        for i in range(1, self.lives1 + 1):
            self.screen.blit(self.heart, (self.screenW - margin*i - 20, height))

        for i in range(1, self.lives2 + 1):
            self.screen.blit(self.heart, (self.screenW - margin*i - 20, 
            height + 40))
        
        if not self.singlePlayer:
            self.drawText("p1", 25, 
            RED, self.screenW - margin/3, height)
            self.drawText("p2", 25, 
            BLUE, self.screenW - margin/3, height + 40)
        
    def showStartScreen(self):
        #game start screen
        self.screen.fill((0,0,0))
        self.drawText("JUMP CAT", 50, (200,200,0), WIDTH/2, HEIGHT/4)

        self.drawText("[Press a key to play]", 30, 
        WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        
        self.buttonCol = (0,200,250)
        self.instructButton = Button(self, self.buttonCol, self.screenW//2, 
        self.screenH//2.5, 220, 45, 'Instructions')
        self.instructButton.draw(self.screen)
        
        self.settingsButton = Button(self, self.buttonCol, self.screenW//2, 
        self.screenH//2.5 + 80, 220, 45, 'Settings')
        self.settingsButton.draw(self.screen)
        
        self.editorButton = Button(self, self.buttonCol, self.screenW//2, 
        self.screenH//2.5 + 160, 220, 45, 'Level Editor')
        self.editorButton.draw(self.screen)
            
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
            
    def showInstructions(self):
        self.screen.fill((0,0,0))
        margin = 80
        self.drawText("* ~ Arrow Keys to move, Space to shoot", 30, 
                (0,200,200), WIDTH/2, HEIGHT/4)

        self.drawText("* ~ Dodge Enemy Bees and Rain Clouds", 30, 
                (0,200,200), WIDTH/2, HEIGHT/4 + margin)

        self.drawText("* ~ Collect Extra Lives and Coins to earn points", 30, 
                (0,200,200), WIDTH/2, HEIGHT/4 + margin*2)

        self.drawText("[Press a key to return]", 30, 
                (200,200,200), WIDTH/2, HEIGHT/4 + margin*3)
        pg.display.flip()

        self.wait_for_key()
    
    def drawLevelEditor(self):
        #Game Loop - draw
        self.screen.fill((50,150,250))
        
        self.drawText("Click to insert clouds!" + str(self.level), 
        40, (250,250,0), 80, 15)
        
        self.drawText("Dist: " + str(self.distance), 
        40, (250,250,0), 80, 50)
        
        pg.display.flip()
    
    def showSettings(self):
        self.screen.fill((0,0,0))
        margin = 80
        
        self.buttonCol, self.buttonCol2 = (0,200,250), (0,200,250)
        if self.singlePlayer: self.buttonCol = (250,250,250)
        else: self.buttonCol2 = (250, 250, 250)
        self.singlePlayerButton = Button(self, self.buttonCol, self.screenW//2, 
        self.screenH//3, 200, 50, 'Single Player')
        self.singlePlayerButton.draw(self.screen)
        
        self.twoPlayerButton = Button(self, self.buttonCol2, self.screenW//2, 
        self.screenH//3 + margin, 200, 50, 'Two Player')
        self.twoPlayerButton.draw(self.screen)
                
        self.drawText("[Press a key to return]", 30, 
                (200,200,200), WIDTH/2, HEIGHT/4 + margin*3)
        pg.display.flip()

        self.wait_for_key()
    
    #wait for key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                mousePos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    waiting = False
                    self.playing = False
                    self.running = False
                elif self.mode == "start":
                    if self.instructButton.isOver(mousePos):
                        if event.type == pg.MOUSEBUTTONDOWN:
                            waiting = False
                            self.mode = "instructions"
                    elif self.settingsButton.isOver(mousePos):
                        if event.type == pg.MOUSEBUTTONDOWN:
                            waiting = False
                            self.mode = "settings"
                elif self.mode == "settings":
                    if self.singlePlayerButton.isOver(mousePos):
                        if event.type == pg.MOUSEBUTTONDOWN:
                            waiting = False
                            self.singlePlayer = True
                    elif self.twoPlayerButton.isOver(mousePos):
                        if event.type == pg.MOUSEBUTTONDOWN:
                            waiting = False
                            self.singlePlayer = False
                if event.type == pg.KEYDOWN:
                    waiting = False
                    if self.mode == "start": 
                        self.startGame()
                    else: self.mode = "start"
                    
    def startGame(self):
        self.mode = "game"
        self.player = Player(self)
        if not self.singlePlayer:
            self.player2 = Player2(self)
            self.lives2 = 3
            
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
    
    #animate frames
    def animate(self):
        now = pg.time.get_ticks()
    
#Run game!
g = Game()
while g.running:
    g.new(g.singlePlayer)
    g.showGameOver()
pg.quit()
                