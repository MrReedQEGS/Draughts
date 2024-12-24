##############################################################################
# DETAILS
#  Attempt 1 at an othello game
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
# Store the board before a move and then undo will be easy
# Splash screen - state machine.  Ability to have another go
# music on off button

##############################################################################
# IMPORTS
##############################################################################
import pygame, random, time
from pygame.locals import *
from othelloClasses import perpetualTimer,MyGameGrid,MyClickableImageButton

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
pygame.display.set_caption('Othello - Mark Reed (c) 2024')

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREY = (150,150,150)
COL_RED = (255,0,0)
COL_BLUE = (0,0,255)
COL_DARK_BLUE = (35, 5, 250)
BACK_FILL_COLOUR = COL_WHITE
backImageName = "./images/othello blank grid.jpg"
turnIndicatorImageName = "./images/turnIndicator.jpg"
scoreImageName = "./images/score.jpg"
gameOverImageName = "./images/gameOver.jpg"
undoImageName = "./images/Undo.jpg"
undoImageGreyName = "./images/UndoGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImageGreyName = "./images/MuteGrey.jpg"
infoImageName = "./images/Info.jpg"
infoImageGreyName = "./images/InfoGrey.jpg"

TOP_LEFT = (35,22)
TOP_RIGHT = (452,22)
BOT_LEFT = (35,438)
BOT_RIGHT = (452,438)
GRID_SIZE_X = 52
GRID_SIZE_Y = 52
A1_location = (62,50)  #Used to draw pieces in the correct place!
PIECE_SIZE = 20

p1Score = 2
p2Score = 2

#sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound("./sounds/click.mp3")
pygame.mixer.music.load("./sounds/relaxing-music.mp3") 
pygame.mixer.music.play(-1,0.0)
musicOn = True

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 16)
p1ScoreSurface = my_font.render('2', False, (0, 0, 0))
p2ScoreSurface = my_font.render('2', False, (0, 0, 0))

running = True

turn = COL_BLACK
turnIndicatorYPos = 24
alwaysShowNextMoves = True
nextMoveColour = (50,50,200)
lighter = True # Controls the direction of the colour fade on the next move squares
nextMoveThickness = 1

#Timer callbacks
def OneSecondCallback():
    #Update game time
    global gameTime
    gameTime = gameTime + 1

def ZeroPointOneSecondCallback():
    global nextMoveColour,lighter,nextMoveThickness

    if(lighter == True):
        if(nextMoveColour[0] < 120):
            nextMoveColour = (nextMoveColour[0]+10,nextMoveColour[1]+10,200)
            nextMoveThickness = nextMoveThickness + 1
        else:  
            lighter = False
    else:
        if(nextMoveColour[0] > 50):
            nextMoveColour = (nextMoveColour[0]-10,nextMoveColour[1]-10,200)
            nextMoveThickness = nextMoveThickness - 1
        else:  
            lighter = True

    
gameTime = 0
gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
DELAY_1 = 1
myOneSecondTimer = None
if(myOneSecondTimer == None):
    myOneSecondTimer = perpetualTimer(DELAY_1,OneSecondCallback)
    myOneSecondTimer.start()

DELAY_01 = 0.05
myZeroPointOneTimer = None
if(myZeroPointOneTimer == None):
    myZeroPointOneTimer = perpetualTimer(DELAY_01,ZeroPointOneSecondCallback)
    myZeroPointOneTimer.start()

##############################################################################
# SUB PROGRAMS
##############################################################################
def MakeTheStartingBoard():
    global turn,turnIndicatorYPos
    turn = COL_BLACK
    turnIndicatorYPos = 24
    theGameGrid.BlankTheGrid()
    theGameGrid.SetGridItem((3,3),WHITE_PIECE)
    theGameGrid.SetGridItem((4,3),BLACK_PIECE)
    theGameGrid.SetGridItem((4,4),WHITE_PIECE)
    theGameGrid.SetGridItem((3,4),BLACK_PIECE)
    UpdateScores()

def TurnOffTimers():
        
    global myOneSecondTimer,myZeroPointOneTimer
    if(myOneSecondTimer!=None):
        myOneSecondTimer.cancel()
        myOneSecondTimer = None
        if(DEBUG_ON):
            print("Turnning off timer...myOneSecondTimer")

    if(myZeroPointOneTimer!=None):
        myZeroPointOneTimer.cancel()
        myZeroPointOneTimer = None
        if(DEBUG_ON):
            print("Turnning off timer...myZeroPointOneTimer")

def GetEmptySquares():
    emptySquares = []
    #find everywhere that does not have a piece on it
    for i in range(8):
        for j in range(8):
            if(theGameGrid.GetGridItem((i,j)) == 0):
                emptySquares.append((i,j))

    return emptySquares

def GetCurrentPiece():
    currentPiece = BLACK_PIECE
    oppositePiece = WHITE_PIECE
    if(turn == COL_WHITE):
        currentPiece = WHITE_PIECE
        oppositePiece = BLACK_PIECE
    return currentPiece,oppositePiece

def UpdateScores():
    global p1ScoreSurface,p2ScoreSurface,p1Score,p2Score

    p1Score = 0
    p2Score = 0

    for i in range(8):
        for j in range(8):
            currentCellItem = theGameGrid.GetGridItem((i,j))
            if(currentCellItem == EMPTY_SQUARE):
                continue
            elif(currentCellItem == BLACK_PIECE):
                p1Score = p1Score + 1
            elif(currentCellItem == WHITE_PIECE):
                p2Score = p2Score + 1

    p1ScoreSurface = my_font.render(str(p1Score), False, (0, 0, 0))
    p2ScoreSurface = my_font.render(str(p2Score), False, (0, 0, 0))

def LoadImages():
    global backImage,turnIndicatorImage,scoreImage,undoImage,undoGreyImage,muteImage,muteGreyImage
    global infoImage,infoGreyImage,gameOverImage
 
    backImage = pygame.image.load(backImageName).convert()
    turnIndicatorImage = pygame.image.load(turnIndicatorImageName).convert()
    scoreImage = pygame.image.load(scoreImageName).convert()
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
    gameOverImage = pygame.image.load(gameOverImageName).convert()

        
def SwapTurn():
    global turn,turnIndicatorYPos
    if(turn == COL_WHITE):
        turn = COL_BLACK
        turnIndicatorYPos = 24
    else:
        turn = COL_WHITE
        turnIndicatorYPos = 50

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

def DrawTurnMarker():
    pygame.draw.rect(surface, COL_DARK_BLUE, pygame.Rect(487,turnIndicatorYPos, 28, 27),2)
            
def DrawTheCurrentGameGrid():

    for row in range(8):
        for col in range(8):

            #Get current piece
            thisPiece =  theGameGrid.GetGridItem((col,row))

            #find out what colour we are drawing
            pieceCol = COL_WHITE
            if(thisPiece == EMPTY_SQUARE):
                continue # its a blank square
            elif (thisPiece == BLACK_PIECE):
                pieceCol = COL_BLACK
            
            pygame.draw.circle(surface, pieceCol, (A1_location[0] + col*GRID_SIZE_X, A1_location[1] + row*GRID_SIZE_Y), PIECE_SIZE)

def CheckVerticalUp(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for vert run UP
    numInRun = 0
    for i in range(row-1,-1,-1):
        thisGridItem = theGameGrid.GetGridItem((col,i))
        if( thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(row-1,row-1-numInRun,-1):
                theGameGrid.SetGridItem((col,i),currentPiece)
    
        if(DEBUG_ON):
            print("Vertical UP move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckVerticalDown(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for vert run DOWN
    numInRun = 0
    for i in range(row+1,8):
        thisGridItem = theGameGrid.GetGridItem((col,i))
        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(row+1,row+1+numInRun):
                theGameGrid.SetGridItem((col,i),currentPiece)
        
        if(DEBUG_ON):
            print("Vertical down move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckHorizontalRight(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for horizontal run ->
    numInRun = 0
    for i in range(col+1,8):

        thisGridItem = theGameGrid.GetGridItem((i,row))

        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(col+1,col+1+numInRun):
                theGameGrid.SetGridItem((i,row),currentPiece)
    
    if(DEBUG_ON):
        print("Horizontal right move allowed? " + str(runFound))
        print("Run found : {} ".format(numInRun))

    return runFound

def CheckHorizontalLeft(currentPiece,oppositePiece,row,col,applyTheMove=True):
    runFound = True
    #look for horizontal run <-
    numInRun = 0
    for i in range(col-1,-1,-1):
        thisGridItem = theGameGrid.GetGridItem((i,row))
        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break  # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(col-1,col-1-numInRun,-1):
                theGameGrid.SetGridItem((i,row),currentPiece)
   
        if(DEBUG_ON):
            print("Horizontal left move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckDiagonalDownRight(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for diagonal run DOWN RIGHT
    numInRun = 0
    rowNeedTo7 = 7 - row
    colNeededTo7 = 7 - col
    numOfLoops = min(rowNeedTo7,colNeededTo7)

    for i in range(1,numOfLoops):
        thisGridItem = theGameGrid.GetGridItem((col +i,row+i))
        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(numInRun):
                theGameGrid.SetGridItem((col+1+i,row+1+i),currentPiece)
        
        if(DEBUG_ON):
            print("diagonal right down move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckDiagonalDownLeft(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for diagonal run DOWN LEFT
    numInRun = 0
    rowNeedTo7 = 7-row
    colNeededTo0 = col
    numOfLoops = min(rowNeedTo7,colNeededTo0)

    for i in range(1,numOfLoops):
        thisGridItem = theGameGrid.GetGridItem((col-i,row+i))
        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(numInRun):
                theGameGrid.SetGridItem((col-1-i,row+1+i),currentPiece)
        
        if(DEBUG_ON):
            print("diagonal left down move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckDiagonalUpLeft(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for diagonal run UP LEFT
    numInRun = 0
    rowNeedTo0 = row
    colNeededTo0 = col
    numOfLoops = min(rowNeedTo0,colNeededTo0)

    for i in range(0,numOfLoops):
        thisGridItem = theGameGrid.GetGridItem((col-1-i,row-1-i))
        if(thisGridItem== EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(numInRun):
                theGameGrid.SetGridItem((col-1-i,row-1-i),currentPiece)
        
        if(DEBUG_ON):
            print("diagonal left up move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckDiagonalUpRight(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for diagonal run UP RIGHT
    numInRun = 0
    rowNeedTo0 = row
    colNeededTo7 = 7-col
    numOfLoops = min(rowNeedTo0,colNeededTo7)

    for i in range(0,numOfLoops):
        thisGridItem = theGameGrid.GetGridItem((col+1+i,row-1-i))
        if(thisGridItem == EMPTY_SQUARE):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(thisGridItem == oppositePiece):
            numInRun = numInRun + 1
        if(thisGridItem == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(numInRun):
                theGameGrid.SetGridItem((col+1+i,row-1-i),currentPiece)
        
        if(DEBUG_ON):
            print("diagonal right up move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def IsMoveAllowed(somecol, somerow, applyTheMove):
    #Not all moves are valid!!
    #1 - Cannot move outside the grid
    #2 - Cannot add where a piece already is
    #3 - It must be a legal move that causes pieces to flip
    #      B W W W W b <--- HERE IS ALLOWED
    #
    #     resulting in this...
    #      B B B B B b <-- The grid after the "flipping"

    atLeastOneRunWasFound = False

    #who is playing this move?
    currentPiece, oppositePiece = GetCurrentPiece()

    currentGridItem = theGameGrid.GetGridItem((somecol,somerow))

    if(currentGridItem == BLACK_PIECE or currentGridItem == WHITE_PIECE):
        return False  # piece is here...  DO NOT ALLOW the move
    else:
        #Its an empty space...does it make an allowed "run"
        runFound = CheckHorizontalRight(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True
        
        runFound = CheckHorizontalLeft(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckVerticalDown(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True
       
        runFound = CheckVerticalUp(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckDiagonalDownRight(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckDiagonalDownLeft(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckDiagonalUpLeft(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckDiagonalUpRight(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

    return atLeastOneRunWasFound

def ShowNextMoves(gameOver):

    if(gameOver):
        return

    emptySquares = GetEmptySquares()
    
    atLeastOneMove = False

    for square in emptySquares:
        if(IsMoveAllowed(square[0],square[1],False)):
            if(alwaysShowNextMoves):
                atLeastOneMove = True
                pygame.draw.rect(surface, nextMoveColour, pygame.Rect(37+square[0]*GRID_SIZE_X+5,24+square[1]*GRID_SIZE_Y+5, GRID_SIZE_X-10, GRID_SIZE_Y-10),nextMoveThickness)

    if(alwaysShowNextMoves and not atLeastOneMove):
        print("NO MORE MOVES...GAME OVER!!!")
        return False
    else:
        return True

def AddPieceToGrid(col,row):

    currentPiece,oppositePiece = GetCurrentPiece()

    #Only allow the move if the square is not full already...
    if(IsMoveAllowed(col,row,True)):
        theGameGrid.SetGridItem((col,row), currentPiece)
        pygame.mixer.Sound.play(clickSound)
        SwapTurn()
        UpdateScores()
  
def HandleInput(running,gameOver):
    
    global alwaysShowNextMoves,waitingForYesNo

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if(not gameOver):    
            #Toggle grid centre markers?
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_SPACE:
            #        alwaysShowNextMoves = not alwaysShowNextMoves

            #Detect a mouse up
            if event.type == pygame.MOUSEBUTTONUP:

                somePos = pygame.mouse.get_pos()
                
                currentClickX = somePos[0]
                currentClickY = somePos[1]

                if(currentClickX < TOP_LEFT[0] or
                currentClickX > TOP_RIGHT[0] or
                currentClickY < TOP_LEFT[1] or
                currentClickY > BOT_RIGHT[1]):
                    if(DEBUG_ON):
                        print("NOT ON THE BOARD")
                    else:
                        pass

                else:
                    col,row = WhatSquareAreWeIn(somePos)
                    AddPieceToGrid(col,row)
                
    return running

def UndoButtonCallback():
    #Use a TKINTER message box :)
    #Turn events off and then back on to stop pygame picking up the mouse click too!
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP) 
    answer = messagebox.askyesno("Question","Do you really want to undo the last move?")
    if(answer):
        MakeTheStartingBoard()
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
    global alwaysShowNextMoves
    alwaysShowNextMoves = not alwaysShowNextMoves

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

gameOver = False

MakeTheStartingBoard()

gameOverImage = pygame.transform.scale(gameOverImage, (80,80))

theUndoButton = MyClickableImageButton(426,455,undoImage,undoGreyImage,surface,UndoButtonCallback)
theMuteButton = MyClickableImageButton(396,455,muteImage,muteGreyImage,surface,MuteButtonCallback)
theInfoButton = MyClickableImageButton(366,455,infoImage,infoGreyImage,surface,InfoButtonCallback)

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))

    surface.blit(turnIndicatorImage, (460, 0))

    surface.blit(scoreImage, (475, 364))

    surface.blit(p1ScoreSurface, (514,390))
    surface.blit(p2ScoreSurface, (514,416))

    theUndoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theInfoButton.DrawSelf()

    DrawTurnMarker()

    if ShowNextMoves(gameOver) == False:
        gameOver = True
        TurnOffTimers()
        #game over happened!!!

    running = HandleInput(running,gameOver)
   
    if(running):
        DrawTheCurrentGameGrid()

        if(gameOver):
            surface.blit(gameOverImage, (470, 180))
        
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (30,460))

        pygame.display.flip()

TurnOffTimers()

pygame.quit()
