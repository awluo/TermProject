import pygame

class Enemy(object):
    def __init__(self, xc, yc, radius = 50, color = (0, 200, 0)):
        self.x = xc
        self.y = yc
        self.r = radius
        self.hp = 100 #starting health
        self.color = color
        
    #draw monster
    def draw(self, window):
        pygame.draw.circle(window, self.color, 
        (int(self.x), int(self.y)), self.r)
        self.color = (0,200,0) #reset color

    #react to getting hit by bullet
    def getHit(self):
        self.hp -= 10
        
    
    