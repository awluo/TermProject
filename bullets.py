import pygame

class Bullet(object):
    def __init__(self, xc, yc, xVel, r = 5, color = (0,0,250)):
        #bullet attributes
        self.r = r
        self.x = xc
        self.y = yc
        self.xVel = xVel * 20
        self.color = color
    
    #move bullet by velocity
    def move(self):
        self.x += self.xVel
    
    #draw bullet on surface
    def draw(self, window):
        pygame.draw.circle(window, self.color, 
        (int(self.x), int(self.y)), self.r)