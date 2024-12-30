import pygame
##############################################################################
# CLASSES
##############################################################################
class Piece(pygame.sprite.Sprite): 
    def __init__(self, newImage, newPos,newParentSurface): 
        super().__init__() 

        self._image = newImage
        self._pos = newPos
        self._rect = self._image.get_rect()
        self._rect.topleft=(newPos[0],newPos[1])
        self._parentSurface = newParentSurface
        self._king = False
        self._kingFont = pygame.font.SysFont('Comic Sans MS', 16)
        self._kingSurface = self._kingFont.render("K", False, (0, 255, 0))

    def DrawSelf(self):
        self._parentSurface.blit(self._image, (self._pos[0], self._pos[1]))
        if(self._king):
            self._parentSurface.blit(self._kingSurface, (self._pos[0]+17, self._pos[1]+9))
            #pygame.draw.rect(self._parentSurface, (255,0,0), pygame.Rect(self._pos[0]+17, self._pos[1]+17, 10, 10))

    def SetPos(self,newPos):
        self._pos = newPos
        self._rect.topleft=(newPos[0],newPos[1])

    def GetPos(self):
        return self._pos
    
    def ClickedOnMe(self,clickPos):
        if(self._rect.collidepoint(clickPos)):
            return True
        else:
            return False

