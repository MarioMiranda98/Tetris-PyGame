import pygame, sys, time
from pygame.locals import QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN

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
            [100, 50, 10*20 + 9, 20*20 + 9], #[Coordinate X, Coordinate Y, Width, Height] Size and position of rect
            5 #Line's Thickness
        )

        drawBoard(screen, gameMatrix)

        listenToUserInput(gameMatrix, piece)

        if(piece['row'] == 19 or gameMatrix[piece['row'] + 1][piece['column']] != '.'):
            gameMatrix[piece['row']][piece['column']] = 'c'
            piece = createPiece()

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

def drawBoard(screen, gameMatrix):
    whiteColor = (255, 255, 255)
    grayColor = (217, 222, 226)
    gameMatrixColumns = 10
    gameMatrixRows = 20

    for i in range (gameMatrixRows):
        for j in range(gameMatrixColumns):
            if(gameMatrix[i][j] == 'c'):
                if(gameMatrix[i][j] != '.'):
                    drawSingleTetrisBox(screen, i, j, (255, 255, 255), (217, 222, 226))

def drawSingleTetrisBox(screen, row, column, whiteColor, grayColor):
   originX = 100 + 5 + (column * 20 + 1)
   originY = 50 + 5 + (row * 20 +1)

   pygame.draw.rect(screen, grayColor, [originX, originY, 20, 20])
   pygame.draw.rect(screen, whiteColor, [originX, originY, 18, 18]) 

def listenToUserInput(gameMatrix, piece):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if (event.key == K_LEFT and isValidPosition(gameMatrix, piece['row'], piece['column'] - 1)):
                piece['column'] = piece['column'] - 1
            if (event.key == K_RIGHT and isValidPosition(gameMatrix, piece['row'], piece['column'] + 1)):
                piece['column'] = piece['column'] + 1
            if (event.key == K_DOWN and isValidPosition(gameMatrix, piece['row'] + 1, piece['column'])):
                piece['row'] += 1

def isValidPosition(gameMatrix, row, column):
    if not (column >= 0 and column < 10 and row < 20):
        return False
    if(gameMatrix[row][column] != '.'):
        return False

    return True

        
runTetrisGame()