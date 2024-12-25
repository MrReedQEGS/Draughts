import pygame
##############################################################################
# CLASSES
##############################################################################
class Piece(pygame.sprite.Sprite): 
    def __init__(self, newPieceNum, newImage, newPos,newParentSurface): 
        super().__init__() 
  
        self._pieceNum = newPieceNum
        self._image = newImage
        self._pos = newPos
        self._rect = self._image.get_rect()
        self._rect.topleft=(newPos[0],newPos[1])
        self._parentSurface = newParentSurface

    def DrawSelf(self):
        self._parentSurface.blit(self._image, (self._pos[0], self._pos[1]))

    def SetPos(self,newPos):
        self._pos = newPos
        self._rect =(newPos[0],newPos[1])

    def GetPos(self):
        return self._pos
    
    def ClickedOnMe(self,clickPos):
        if(self._rect.collidepoint(clickPos)):
            return True
        else:
            return False

