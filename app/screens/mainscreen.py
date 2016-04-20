from datetime import datetime
import pygame
from pygame.rect import Rect

from modules.focus import ProcessFocus
from modules.stacking import ProcessStacking
from widgets import colours
from widgets.background import LcarsBackgroundImage
from widgets.gifimage import LcarsGifImage
from widgets.screen import LcarsScreen
from widgets.sprite import LcarsMoveToMouse
from widgets.lcars_widgets import LcarsText


class MainScreen(LcarsScreen):
    def setup(self, all_sprites):
        self.image = None
        self.zoomPoint = None

        # detect focus
        self.focus = ProcessFocus()
        self.focus.start()
        
        # stack images
        self.stack = ProcessStacking()
        self.stack.start()
        self.showStack = False
        
        self.focusText = LcarsText((255,0,0), (17,303), "Focus: xxxxxx")
        
        all_sprites.add(LcarsBackgroundImage("assets/jarvis.png"))
        all_sprites.add(self.focusText)
        #all_sprites.add(LcarsGifImage("assets/jarvis_gadgets.gif", (83, 258)))
        # all_sprites.add(LcarsMoveToMouse(colours.BEIGE))
        
    def setImage(self, image):
        # do background processing
        self.focus.addFrame(image)
        if self.showStack: self.stack.addFrame(image)
        if self.showStack and self.stack.outputFrame is not None:
            image = self.stack.getFrame()

        if (image == None): return
        self.image = pygame.image.frombuffer(image, (len(image[0]), len(image)), 'RGB')
        # change from BGR to RGB
        r, g, b, a = self.image.get_shifts()
        self.image.set_shifts((b, g, r, a))
        
    def update(self, screenSurface, fpsClock):
        self.focusText.renderText("Focus: %d" % self.focus.focus)
        self.focusText.update(screenSurface)
                           
        if (self.image != None):
            screenSurface.blit(self.image,
                # placement of preview window
                (100, 100),  
                # area of image to display
                Rect(100, 100, self.image.get_width(), self.image.get_height())) 

    def handleEvents(self, event, fpsClock):
        return LcarsScreen.handleEvents(self, event, fpsClock)
    
    def timeStamped(self, fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.now().strftime(fmt).format(fname=fname)

    
