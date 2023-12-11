import pygame as py

class Platform():
    def __init__(self,screen,size,position,path=""):
        self.screen = screen
        self.size = size
        self.position = position
        self.path = path
        self.create_platform()
        self.rect = self.surface.get_rect()
        self.rect.x,self.rect.y = self.position 
    
    def create_platform(self):
        if self.path != "":
            self.surface = py.image.load(self.path)
            self.surface = py.transform.scale(self.surface,self.size)
        else:
            self.surface = py.Surface(self.size)

    def blit_platform(self):
        self.screen.blit(self.surface,self.position)