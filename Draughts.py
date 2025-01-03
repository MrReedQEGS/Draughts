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
#Make it so the pieces go into the grid data structure when you create one.
#
#They need to move around in the data structure as we drag them.  This will allow
#the game to check if a piece is already on a square.  A drag should fail and go back to the 
#picked up location if the user tries to drop a piece on an occupied square
#
#The "bar" and the "box area" must also be in the grid or this will fail when we take pieces off the board.

##############################################################################
# IMPORTS
##############################################################################
import pygame, random, time
from pygame.locals import *
from UsefulClasses import perpetualTimer,MyGameGrid,MyClickableImageButton

import tkinter
from tkinter import messagebox

from DraughtsClasses import Piece

##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Draughts"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

#CREATE THE EMPTY GAME GRID OBJECT
EMPTY_SQUARE = 0
BLACK_PIECE = 1
WHITE_PIECE = 2
theGameGrid = MyGameGrid(8,8,[EMPTY_SQUARE,BLACK_PIECE,WHITE_PIECE],0)

RIGHT_MOUSE_BUTTON = 3

DEBUG_ON = False

GRID_SIZE_X = 52
GRID_SIZE_Y = 52
TOP_LEFT = (26,28)

SCREEN_WIDTH = 678
SCREEN_HEIGHT = 504

BUTTON_X_VALUE = 526
BUTTON_Y_VALUE  = 472
BUTTON_WIDTH = 30

gridLinesOn = False

GAME_TIME_X = 2
GAME_TIME_Y = BUTTON_Y_VALUE + 5

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

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
eyeImageName = "./images/Eye.jpg"
eyeImageGreyName = "./images/EyeGrey.jpg"
restartImageName = "./images/Restart.jpg"
restartImageGreyName = "./images/RestartGrey.jpg"

player1PieceImageName = "./images/player1Piece.png"
player2PieceImageName = "./images/player2Piece.png"

PIECE_SIZE = 20
draggingPiece = None

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
    global eyeImage,eyeGreyImage,restartImage,restartGreyImage
    global infoImage,infoGreyImage,player1PieceImage,player2PieceImage
 
    backImage = pygame.image.load(backImageName).convert()

    #Load an image with a white background and set the white to transparent.
    #Will only work if the background is all properly white 255,255,255
    player1PieceImage = pygame.image.load(player1PieceImageName)
    player1PieceImage = pygame.transform.scale(player1PieceImage, (43, 43))  #change size first before doing alpha things
    player1PieceImage.set_colorkey((255,255,255))
    player1PieceImage.convert_alpha()

    player2PieceImage = pygame.image.load(player2PieceImageName)
    player2PieceImage = pygame.transform.scale(player2PieceImage, (43, 43))  #change size first before doing alpha things
    player2PieceImage.set_colorkey((255,255,255))
    player2PieceImage.convert_alpha()
    
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
    eyeImage = pygame.image.load(eyeImageName).convert()
    eyeGreyImage = pygame.image.load(eyeImageGreyName).convert()
    restartImage = pygame.image.load(restartImageName).convert()
    restartGreyImage = pygame.image.load(restartImageGreyName).convert()
        
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
    
    global waitingForYesNo,draggingPiece

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            currentMousePos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
                #print ("You pressed the right mouse button")
                for piece in allPieces:
                    if(piece.ClickedOnMe(currentMousePos)):
                        piece._king = not piece._king
            else:
                #did we click on a piece?
                for piece in allPieces:
                    if(piece.ClickedOnMe(currentMousePos)):
                        draggingPiece = piece
                        #The last piece in the allpieces list is draw last, so move the dragged one to last
                        #in the list to make it draw on top of every other piece as you drag it...simples!
                        allPieces.remove(draggingPiece)
                        allPieces.append(draggingPiece)

           
        elif event.type == pygame.MOUSEBUTTONUP:
            currentMousePos = pygame.mouse.get_pos()
            currentSquare = WhatSquareAreWeIn(currentMousePos)
            #print("Square dropped in : ", currentSquare)

            #Let go of a piece if we have one
            if(draggingPiece != None):
                pygame.mixer.Sound.play(clickSound)
                somePos = draggingPiece.GetPos()
                dropLocation = [TOP_LEFT[0] + currentSquare[0]*GRID_SIZE_X+5,TOP_LEFT[1] + currentSquare[1]*GRID_SIZE_Y+5]
                draggingPiece.SetPos(dropLocation)
                draggingPiece = None
                  
    return running

def EyeButtonCallback():
    global gridLinesOn
    gridLinesOn = not gridLinesOn

def UndoButtonCallback():
    print("undo pressed...")

def RestartButtonCallback():

    #Use a TKINTER message box :)
    #Turn events off and then back on to stop pygame picking up the mouse click too!
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP) 
    answer = messagebox.askyesno("Question","Do you really to reset the whole game?")
    if(answer):
        PutPiecesInTheBox()
    pygame.event.set_allowed(None)


def MuteButtonCallback():
    global musicOn
    if(musicOn):
        musicOn = False
        pygame.mixer.music.pause()
    else:
        musicOn = True
        pygame.mixer.music.unpause()
            
def InfoButtonCallback():
   print("Info pressed")

def DrawGreenLinesOverTheBoard(width): 
    if(gridLinesOn):
        for i in range(9):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[1]),(TOP_LEFT[0]+i*GRID_SIZE_X, TOP_LEFT[0] + 8*GRID_SIZE_Y),width)
        for i in range(9):
            pygame.draw.line(surface,COL_GREEN,(TOP_LEFT[0], 27+i*GRID_SIZE_Y),(TOP_LEFT[0]+8*GRID_SIZE_X, TOP_LEFT[1]+i*GRID_SIZE_Y),width)

def PutPiecesInTheBox():
    global allPieces
    allPieces = []
    for i in range(8):
        someGamePiece = Piece(player1PieceImage,[30+GRID_SIZE_X*9, 33+GRID_SIZE_Y*i],surface)
        allPieces.append(someGamePiece)
    for i in range(4):
        someGamePiece = Piece(player1PieceImage,[30+GRID_SIZE_X*10, 33+GRID_SIZE_Y*i],surface)
        allPieces.append(someGamePiece)
    for i in range(4):
        someGamePiece = Piece(player2PieceImage,[30+GRID_SIZE_X*10, 33+GRID_SIZE_Y*(4+i)],surface)
        allPieces.append(someGamePiece)
    for i in range(8):
        someGamePiece = Piece(player2PieceImage,[30+GRID_SIZE_X*11, 33+GRID_SIZE_Y*i],surface)
        allPieces.append(someGamePiece)
    
    

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

theRestartButton = MyClickableImageButton(BUTTON_X_VALUE,BUTTON_Y_VALUE,restartImage,restartGreyImage,surface,RestartButtonCallback)
theEyeButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*1,BUTTON_Y_VALUE,eyeImage,eyeGreyImage,surface,EyeButtonCallback)
theInfoButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*2,BUTTON_Y_VALUE,infoImage,infoGreyImage,surface,InfoButtonCallback)
theMuteButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*3,BUTTON_Y_VALUE,muteImage,muteGreyImage,surface,MuteButtonCallback)
theUndoButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*4,BUTTON_Y_VALUE,undoImage,undoGreyImage,surface,UndoButtonCallback)

allPieces = []
PutPiecesInTheBox()

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (1, 1))

    DrawGreenLinesOverTheBoard(3)

    theRestartButton.DrawSelf()
    theEyeButton.DrawSelf()
    theInfoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theUndoButton.DrawSelf()

    running = HandleInput(running)
   
    #We may be dragging a particular piece!
    currentMousePos = pygame.mouse.get_pos()    
    if(draggingPiece != None):  
        dragLocation = [currentMousePos[0]-GRID_SIZE_X//2,currentMousePos[1]-GRID_SIZE_Y//2]
        draggingPiece.SetPos(dragLocation)

    for piece in allPieces:
        piece.DrawSelf()
       
    if(running):
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (GAME_TIME_X,GAME_TIME_Y))
        pygame.display.flip()

TurnOffTimers()

pygame.quit()