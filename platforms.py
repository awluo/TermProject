import pygame

class Platform(object):
    def __init__(self, cx, cy, h = 10, w = 150):
        # An platform has a position and size
        self.x = cx
        self.y = cy
        self.h = h #height
        self.w = w #width

    def draw(self, screen, color = (0,200,0)):
        #draw platform
        pygame.draw.rect(screen, color, [self.x - self.w/2,
         self.y - self.h/2, 
         self.w, self.h], 2)
    