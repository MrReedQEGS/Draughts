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
# VARIABLES
##############################################################################

#CREATE THE EMPTY GAME GRID OBJECT
EMPTY_SQUARE = 0
BLACK_PIECE = 1
WHITE_PIECE = 2
theGameGrid = MyGameGrid(8,8,[EMPTY_SQUARE,BLACK_PIECE,WHITE_PIECE],0)

DEBUG_ON = False

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 500

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
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

GRID_SIZE_X = 52
GRID_SIZE_Y = 52
TOP_LEFT = (25,27)

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
    global infoImage,infoGreyImage
 
    backImage = pygame.image.load(backImageName).convert()
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

        letters = ["a","b","c","d","e","f","g","h"]
        print("{}{}".format(letters[col],row+1))

    return col,row

def HandleInput(running):
    
    global waitingForYesNo

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:

            somePos = pygame.mouse.get_pos()
            print(somePos)
                
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
    print("Info pressed...")

def DrawGreenLinesOverTheBoard(width): 
    for i in range(9):
        pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1]),(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[0] + 8*GRID_SIZE_Y),width)
    for i in range(9):
        pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0], 27+i*GRID_SIZE_Y),(TOP_LEFT[0]+8*GRID_SIZE_X, TOP_LEFT[1]+i*GRID_SIZE_Y),width)


##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

theUndoButton = MyClickableImageButton(426,455,undoImage,undoGreyImage,surface,UndoButtonCallback)
theMuteButton = MyClickableImageButton(396,455,muteImage,muteGreyImage,surface,MuteButtonCallback)
theInfoButton = MyClickableImageButton(366,455,infoImage,infoGreyImage,surface,InfoButtonCallback)

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))

    DrawGreenLinesOverTheBoard(3)
    

    theUndoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theInfoButton.DrawSelf()

    running = HandleInput(running)
   
    if(running):
        
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (30,460))

        pygame.display.flip()

TurnOffTimers()

pygame.quit()
