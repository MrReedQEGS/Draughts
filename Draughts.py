##############################################################################
# DETAILS
#  Attempt 1 at an draughts game
#  Mr Reed - Dec 2024
#
#  Sounds 
#  https://pixabay.com/sound-effects/search/clicks/
#
#  Music
#  https://pixabay.com/music/search/relaxing%20game%20music/
#
##############################################################################

#To do
#Get a simple grid going
#Starting pieces drawn
#Ability to move a piece anywhere

##############################################################################
# IMPORTS
##############################################################################
import pygame, random, time
from pygame.locals import *
from UsefulClasses import perpetualTimer,MyGameGrid,MyClickableImageButton

import tkinter
from tkinter import messagebox

##############################################################################
# CLASSES
##############################################################################
class Piece(pygame.sprite.Sprite): 
    def __init__(self, newImage, newPos,newParentSurface): 
        super().__init__() 
  
        self.image = newImage
        self.pos = newPos
        self.rect = self.image.get_rect()
        self.parentSurface = newParentSurface

    def DrawSelf(self):
        print("I live at ", self.pos)

##############################################################################
# VARIABLES
##############################################################################

#CREATE THE EMPTY GAME GRID OBJECT
EMPTY_SQUARE = 0
BLACK_PIECE = 1
WHITE_PIECE = 2
theGameGrid = MyGameGrid(8,8,[EMPTY_SQUARE,BLACK_PIECE,WHITE_PIECE],0)

DEBUG_ON = True

GRID_SIZE_X = 52
GRID_SIZE_Y = 52
TOP_LEFT = (26,28)

SCREEN_WIDTH = 647
SCREEN_HEIGHT = 504

BUTTON_X_VALUE = 556
BUTTON_Y_VALUE  = 472

gridLinesOn = False

GAME_TIME_X = 2
GAME_TIME_Y = BUTTON_Y_VALUE + 5

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption('Draughts - Mark Reed (c) 2024')

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREEN = (0,255,0)
BACK_FILL_COLOUR = COL_WHITE

backImageName = "./images/draughts grid.jpg"
undoImageName = "./images/Undo.jpg"
undoImageGreyName = "./images/UndoGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImageGreyName = "./images/MuteGrey.jpg"
infoImageName = "./images/Info.jpg"
infoImageGreyName = "./images/InfoGrey.jpg"

player1PieceImageName = "./images/player1Piece.png"

A1_location = (62,50)  #Used to draw pieces in the correct place!
PIECE_SIZE = 20

#sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound("./sounds/click.mp3")
pygame.mixer.music.load("./sounds/relaxing-music.mp3") 

musicOn = False
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.pause()

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 16)

running = True

turn = COL_BLACK

#Timer callbacks
def OneSecondCallback():
    #Update game time
    global gameTime
    gameTime = gameTime + 1

gameTime = 0
gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
DELAY_1 = 1
myOneSecondTimer = None
if(myOneSecondTimer == None):
    myOneSecondTimer = perpetualTimer(DELAY_1,OneSecondCallback)
    myOneSecondTimer.start()

##############################################################################
# SUB PROGRAMS
##############################################################################
def TurnOffTimers():
        
    global myOneSecondTimer
    if(myOneSecondTimer!=None):
        myOneSecondTimer.cancel()
        myOneSecondTimer = None
        if(DEBUG_ON):
            print("Turnning off timer...myOneSecondTimer")

def LoadImages():
    global backImage,undoImage,undoGreyImage,muteImage,muteGreyImage
    global infoImage,infoGreyImage,player1PieceImage
 
    backImage = pygame.image.load(backImageName).convert()

    #Load an image with a white background and set the white to transparent.
    #Will only work if the background is all properly white 255,255,255
    player1PieceImage = pygame.image.load(player1PieceImageName)
    player1PieceImage = pygame.transform.scale(player1PieceImage, (43, 43))  #change size first before doing alpha things
    player1PieceImage.set_colorkey((255,255,255))
    player1PieceImage.convert_alpha()
    
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
        
def WhatSquareAreWeIn(aPosition):
    #Find out what square somebody clicked on.
    #For example, if we click top left the the answer is row 1 col 1  (aka  "a1")
    currentClickX = aPosition[0]
    currentClickY = aPosition[1]
   
    adjustedX = currentClickX-TOP_LEFT[0]
    col = adjustedX//(GRID_SIZE_X+1) #The +1 in the brackets seems to fix the identifcation of col 6 to 7 which was a bit out?
   
    adjustedY = currentClickY-TOP_LEFT[1]
    row = adjustedY//(GRID_SIZE_Y)
   
    if DEBUG_ON:
        print("Current x = {}\nCurrrent y = {}".format(currentClickX,currentClickY))
        print("Col  =  {}".format(col))
        print("row  =  {}".format(row))

    return col,row

def HandleInput(running):
    
    global waitingForYesNo

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            somePos = pygame.mouse.get_pos()
            currentSquare = WhatSquareAreWeIn(somePos)
                
    return running

def UndoButtonCallback():
    print("undo pressed...")

def MuteButtonCallback():
    global musicOn
    if(musicOn):
        musicOn = False
        pygame.mixer.music.pause()
    else:
        musicOn = True
        pygame.mixer.music.unpause()
            
def InfoButtonCallback():
    global gridLinesOn
    gridLinesOn = not gridLinesOn

def DrawGreenLinesOverTheBoard(width): 
    if(gridLinesOn):
        for i in range(9):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1]),(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[0] + 8*GRID_SIZE_Y),width)
        for i in range(9):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0], 27+i*GRID_SIZE_Y),(TOP_LEFT[0]+8*GRID_SIZE_X, TOP_LEFT[1]+i*GRID_SIZE_Y),width)

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

theUndoButton = MyClickableImageButton(BUTTON_X_VALUE + 30*2,BUTTON_Y_VALUE,undoImage,undoGreyImage,surface,UndoButtonCallback)
theMuteButton = MyClickableImageButton(BUTTON_X_VALUE + 30,BUTTON_Y_VALUE,muteImage,muteGreyImage,surface,MuteButtonCallback)
theInfoButton = MyClickableImageButton(BUTTON_X_VALUE,BUTTON_Y_VALUE,infoImage,infoGreyImage,surface,InfoButtonCallback)

someGamePiece = Piece(player1PieceImage,(30, 33))

allPieces = []
allPieces.append(someGamePiece)

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (1, 1))

    DrawGreenLinesOverTheBoard(3)

    for piece in allPieces:
        piece.DrawSelf()
    
    theUndoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theInfoButton.DrawSelf()

    running = HandleInput(running)
   
    if(running):
        
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (GAME_TIME_X,GAME_TIME_Y))

        pygame.display.flip()

TurnOffTimers()

pygame.quit()