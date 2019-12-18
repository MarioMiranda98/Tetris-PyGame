import pygame, sys, time
from pygame.locals import QUIT, KEYUP, K_ESCAPE 

BLUE = (0, 0, 155)
BOX_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_WIDTH = 10

def runTetrisGame(): 
    pygame.init() #Start of the game engine
    windowSize =(640, 480) #Frame measure
    screen = pygame.display.set_mode(windowSize) #Creating a window
    pygame.display.set_caption('My Tetris') #Set the title on the frame
    gameMatrix = createGameMatrix()

    lastTimePieceMoved = time.time()
    piece = createPiece()

    while True:
        screen.fill((0, 0, 0))#background 

        if(time.time() - lastTimePieceMoved > 1):
            piece['row'] = piece['row'] + 1
            lastTimePieceMoved = time.time()

        drawPiece(screen, piece)

        pygame.draw.rect(
            screen, #Where I am going to paint
            BLUE, #The color
            [100, 50, 10*20, 20*20], #[Coordinate X, Coordinate Y, Width, Height] Size and position of rect
            5 #Line's Thickness
        )

        pygame.display.update()

        

        for event in pygame.event.get(QUIT): #Catch the events
            pygame.quit()#Exit of the game
            sys.exit() #terminate the program

def createGameMatrix():
    gameMatrixColumns = 10
    gameMatrixRows = 20
    matrix = []
    for row in range(gameMatrixRows):
        newRow = []
        for column in range(gameMatrixColumns):
            newRow.append('.')
        matrix.append(newRow)

    return matrix

def createPiece():
    piece = {}
    piece['row'] = 0
    piece['column'] = 4
    
    return piece

def drawPiece(screen, piece):
    whiteColor = (255, 255, 255)
    grayColor = (217, 222, 226)

    originX = 100 + 5 + (piece['column'] * 20 + 1)
    originY = 50 + 5 + (piece['row'] * 20 + 1)
    
    pygame.draw.rect(screen, grayColor, [originX, originY, 20, 20])
    pygame.draw.rect(screen, whiteColor, [originX, originY, 18, 18])
    

runTetrisGame()