import pygame, sys, time, random
from pygame.locals import QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN

BLUE = (0, 0, 155)
BOX_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_WIDTH = 10

S_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '..cc.',
    '.cc..',
    '.....'
]]

S_INVERTED_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '.cc..',
    '..cc.',
    '.....'
]]

I_SHAPE_TEMPLATE = [[
    '..c..',
    '..c..',
    '..c..',
    '..c..',
    '.....'
]]

O_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '.cc..',
    '.cc..',
    '.....'
]]

L_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '.c...',
    '.ccc.',
    '.....'
]]

L_INVERTED_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '...c.',
    '.ccc.',
    '.....'
]]

T_SHAPE_TEMPLATE = [[
    '.....',
    '.....',
    '..c..',
    '.ccc.',
    '.....'
]]

def runTetrisGame(): 
    pygame.init() #Start of the game engine
    windowSize =(640, 480) #Frame measure
    screen = pygame.display.set_mode(windowSize) #Creating a window
    pygame.display.set_caption('My Tetris') #Set the title on the frame
    gameMatrix = createGameMatrix()

    lastTimePieceMoved = time.time()
    piece = createPiece()

    score = 0
    while True:
        screen.fill((0, 0, 0))#background 

        if(time.time() - lastTimePieceMoved > 0.3):
            piece['row'] = piece['row'] + 1
            lastTimePieceMoved = time.time()

        #drawPiece(screen, piece)
        drawMovingPiece(screen, piece)
        pygame.draw.rect(
            screen, #Where I am going to paint
            BLUE, #The color
            [100, 50, 10*20 + 9, 20*20 + 9], #[Coordinate X, Coordinate Y, Width, Height] Size and position of rect
            5 #Line's Thickness
        )

        drawBoard(screen, gameMatrix)
        drawScore(screen, score)

        listenToUserInput(gameMatrix, piece)

        if(not isValidPosition(gameMatrix, piece, adjRow = 1)):
            gameMatrix = updateGameMatrix(gameMatrix,piece)
            linesRemoved = removeCompletedLines(gameMatrix)
            score+=linesRemoved
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
    randomShape = random.choice(list(availableTetrisPieces().keys()))
    piece['shape'] = randomShape
    piece['row'] = 0
    piece['column'] = 2
    
    return piece

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
            if (event.key == K_LEFT ) and isValidPosition(gameMatrix, piece, adjColumn = -1):
                piece['column'] -= 1
            elif (event.key == K_RIGHT ) and isValidPosition(gameMatrix, piece, adjColumn = 1):
                piece['column'] += 1
            elif (event.key == K_DOWN) and isValidPosition(gameMatrix, piece, adjRow = 1):
                piece['row'] += 1

def isValidPosition(gameMatrix, piece, adjColumn = 0, adjRow = 0):
    pieceMatrix = availableTetrisPieces()[piece['shape']][0]

    for row in range(5):
        for col in range(5):
            if pieceMatrix[row][col] == '.':
                continue
            if not isOnBoard(piece['row'] + row + adjRow, piece['column'] + col + adjColumn):
                return False
            if gameMatrix[piece['row'] + row + adjRow][piece['column'] + col + adjColumn] != '.':
                return False 

    return True

def drawScore(screen, score):
    myFont = pygame.font.Font('freesansbold.ttf', 18)
    textSurface = myFont.render('Score: %s' % score, True, (255, 255, 255))
    screen.blit(textSurface, (640 - 150, 20))
    

def removeCompletedLines(gameMatrix):
    numLinesRemoved = 0

    for row in range(20):
        if(isLineCompleted(gameMatrix, row)):
            for rowToMoveDown in range(row, 0, -1):
                for column in range(10):
                    gameMatrix[rowToMoveDown][column] = gameMatrix[rowToMoveDown - 1][column]
                
            for x in range(10):
                gameMatrix[0][x] = '.'
            numLinesRemoved += 1

    return numLinesRemoved

def isLineCompleted(gameMatrix, row):
    gameMatrixColumns = 10

    for i in range(gameMatrixColumns):
        if gameMatrix[row][i] != 'c':
            return False 

    return True

def availableTetrisPieces(): 
    return {
        'S' : S_SHAPE_TEMPLATE,
        'SI' : S_INVERTED_SHAPE_TEMPLATE,
        'O' : O_SHAPE_TEMPLATE,
        'L' : L_SHAPE_TEMPLATE,
        'LI' : L_INVERTED_SHAPE_TEMPLATE,
        'T' : T_SHAPE_TEMPLATE
    }

def drawMovingPiece(screen, piece):
    shapeToDraw = availableTetrisPieces()[piece['shape']][0]
    for row in range(5):
        for col in range(5):
            if shapeToDraw[row][col] != '.':
                drawSingleTetrisBox(screen, piece['row'] + row, piece['column'] + col, (255, 255, 255), (217, 222, 226))

def updateGameMatrix(matrix, piece):
    for row in range (5):
        for col in range(5):
            if(availableTetrisPieces()[piece['shape']][0][row][col] != '.'):
                matrix[piece['row'] + row][piece['column'] + col] = 'c'

    return matrix

def isOnBoard(row, column):
    return column >= 0 and column < 10 and row < 20

runTetrisGame()