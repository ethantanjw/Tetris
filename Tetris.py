import math, copy, random
from cmu_112_graphics import *

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Tetris
#################################################
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)
def appPieces():
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    return [iPiece,jPiece,lPiece,oPiece,sPiece,tPiece,zPiece]

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = (gameDimensions())
    app.board = []
    app.emptyColor = "blue"
    for r in range(app.rows):
        app.board += [[app.emptyColor] * app.cols]
    (app.iPiece,app.jPiece,app.lPiece,app.oPiece,app.sPiece,app.tPiece,
    app.zPiece)= (0,0,0,0,0,0,0)
    app.tetrisPieces = [app.iPiece,app.jPiece,app.lPiece,app.oPiece,
    app.sPiece,app.tPiece,app.zPiece]
    app.tetrisPieces = appPieces()
    app.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
    "green", "orange"]
    app.fallingPiece = []
    app.fallingPieceColor = []
    app.fallingPieceRow = -1
    app.fallingPieceCol = -1
    app.selectFallingPiece = newFallingPiece(app)
    app.isGameOver = False
    app.paused = False
    app.score = 0

def keyPressed(app, event):
    if event.key == "Left":
        moveFallingPiece(app,0,-1)
    elif event.key == "Right":
        moveFallingPiece(app,0,+1)
    elif event.key == "Down":
        moveFallingPiece(app,+1,0)
    elif event.key == "Up":
        rotateFallingPiece(app) 
    elif event.key == "Space":
        while moveFallingPiece(app,1,0)==True:
            pass
    if app.isGameOver == True:
        app.paused = True
    if event.key == "r":
        appStarted(app)

def timerFired(app):
    if app.paused == False:
        if moveFallingPiece(app,+1,0) == False:
            placeFallingPiece(app)
            newFallingPiece(app)
            if fallingPieceIsLegal(app) == False:
                app.isGameOver = True
    if app.isGameOver == True:
        app.paused = True

#draw a cell on the board
def drawCell(app,canvas,row,col,color): 
    x0 = app.margin + (col * app.cellSize)
    x1 = app.margin + (col+1) * app.cellSize
    y0 = app.margin + ((row * app.cellSize))
    y1 = app.margin + ((row+1) * app.cellSize)
    canvas.create_rectangle(x0,y0,x1,y1, fill=color,
        outline = "black",width=4)

#draw the board
def drawBoard(app,canvas):
    for r in range(app.rows):
        for c in range(app.cols):
            drawCell(app,canvas,r,c,app.board[r][c])

#generate a new falling piece
import random
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceCol = ((app.cols//2) - 
    ((len(app.tetrisPieces[randomIndex][0]))//2))
    app.fallingPieceRow = 0

#draw the falling piece
def drawFallingPiece(app,canvas): 
    for row in range(len(app.fallingPiece)):
        for cell in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][cell] == True:
                drawCell(app,canvas,(app.fallingPieceRow+row),
                (cell+app.fallingPieceCol),app.fallingPieceColor)
            else: 
                continue

#move the falling piece if the move is legal,
#else backtrack the move if the move is illegal 
def moveFallingPiece(app,drow,dcol):
    app.fallingPieceCol += dcol
    app.fallingPieceRow += drow
    if fallingPieceIsLegal(app) == False:
        app.fallingPieceCol -= dcol
        app.fallingPieceRow -= drow
        return False
    else:
        return True

#checks if the falling piece is within the grid and is not 
#touching another colored piece on the board
def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for cell in range(len(app.fallingPiece[0])):
            x0 = app.margin + (app.fallingPieceCol+cell) * app.cellSize
            x1 = app.margin + (app.fallingPieceCol+cell+1) * app.cellSize
            y0 = app.margin + (app.fallingPieceRow+row) * app.cellSize
            y1 = app.margin + (app.fallingPieceRow+row+1) * app.cellSize
            if ((x0 < app.margin or x1 > app.width - app.margin)  or 
            (y0 < app.margin or y1 > app.height - app.margin)):
                return False  
            elif ((app.board[app.fallingPieceRow+row]
                [app.fallingPieceCol+cell]!=app.emptyColor)and(
                    app.fallingPiece[row][cell]!=False)):
                    return False
    return True

#rotates the falling piece before it is place on the board
def rotateFallingPiece(app):
    tempOldPiece = app.fallingPiece
    tempOldRow = app.fallingPieceRow
    tempOldCol = app.fallingPieceCol
    newPiece = []
    oldNumRows = len(app.fallingPiece)
    oldRow = app.fallingPieceRow
    oldNumCols = len(app.fallingPiece[0])
    oldCol = app.fallingPieceCol
    for r in range(len(app.fallingPiece[0])):
        newPiece += [[None] * (len(app.fallingPiece))]
    for r in range(len(app.fallingPiece)):
        for c in range(len(app.fallingPiece[0])):
            newPiece[c][r] = app.fallingPiece[r][len(app.fallingPiece[0])-1-c]
    app.fallingPiece = newPiece
    app.fallingPieceRow = oldRow + oldNumRows//2 - (len(app.fallingPiece))//2
    app.fallingPieceCol = oldCol + oldNumCols//2 - (len(app.fallingPiece[0]))//2
    if fallingPieceIsLegal(app) == False:
        app.fallingPiece = tempOldPiece
        app.fallingPieceRow = tempOldRow
        app.fallingPieceCol = tempOldCol

#places the falling piece on the board        
def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for cell in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][cell] == True:
                (app.board[app.fallingPieceRow+row]
                [cell+app.fallingPieceCol]) = app.fallingPieceColor
    removeFullRows(app)

#removes a row when the row is filled with colored cells
def removeFullRows(app):
    board2 = []
    fullRows = 0
    for r in range(len(app.board)):
        if app.emptyColor in app.board[r]:
            board2.append(app.board[r])
        else:
            fullRows += 1
    for row in range(len(app.board)-len(board2)):
        board2.insert(0,[app.emptyColor]*app.cols)
    app.board = board2
    app.score += (fullRows ** 2)

#draws the score at the top of the grid
def drawScore(app,canvas):
    canvas.create_text(app.width//2,app.margin//2,text=f"Score: {app.score}",
    fill="black",font="Times 18 bold")
    
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="orange")
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas) 
    drawScore(app,canvas)
    if app.isGameOver == True:
        canvas.create_rectangle(app.margin,app.height//4,app.width-app.margin,
        app.height*(0.75),fill="white")
        canvas.create_text(app.width//2,app.height//2,text="Game Over!",
        fill="black",font="Times 28 bold")  
        canvas.create_text(app.width//2,app.height//2+30,
        text="Press r to restart!",fill="black",font="Times 23 bold")      

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    height = (2 * margin) + (rows * cellSize)
    width = (2 * margin) + (cols * cellSize)
    runApp(width=width, height=height)

#################################################
# main
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()
