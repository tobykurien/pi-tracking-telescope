from widgets.screen import LcarsScreen
from widgets.background import LcarsBackgroundImage
from widgets import colours
from widgets.gifimage import LcarsGifImage
from widgets.sprite import LcarsMoveToMouse
from pygame.rect import Rect
import pygame

class MainScreen(LcarsScreen):
    def setup(self, all_sprites):
        self.image = None
        #all_sprites.add(LcarsBackgroundImage("assets/jarvis.png"))
        #all_sprites.add(LcarsGifImage("assets/jarvis_gadgets.gif", (83, 258)))
        #all_sprites.add(LcarsMoveToMouse(colours.BEIGE))
        
    def setImage(self, image):
        if (image == None): return
        self.image = pygame.image.frombuffer(image, (len(image[0]), len(image)), 'RGB')
        
    def update(self, screenSurface, fpsClock):
        if (self.image != None):
            screenSurface.blit(self.image, 
                Rect(0, 0, self.image.get_width(), self.image.get_height()))
