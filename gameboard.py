#Should be faster

from tetromino import tetromino
from tetrominoQueue import tetrominoQueue 
import numpy as np

ROWS = 28
COLUMNS = 16
BOXSIZE = 30

FRAMES_BEFORE_FALL = 12

class gameboard:
    def __init__(self):
        self.score = 0
        self.piecesPlaced = 0
        self.grid = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        for c in range(COLUMNS):
            for r in range(ROWS):
                if c < 3 or c > 12 or r < 4:
                    self.grid[r][c] = 8
        self.queue = tetrominoQueue()
        self.currentPiece = self.queue.getPiece()
        self.addPiece(self.currentPiece)
        self.gameOver = False
        self.x = 0
        self.y = 0
        self.stallFrames = FRAMES_BEFORE_FALL

    def addPiece(self, tetromino):
        self.currentPiece = tetromino
        x = tetromino.x
        y = tetromino.y
        canPlace = True
        for r in range(4):
            for c in range(4):
                if tetromino.arrangement[r][c] != 0:
                    if self.grid[r+y][c+x] != 0:
                        canPlace = False
                    self.grid[r+y][c+x] = tetromino.arrangement[r][c]
        return canPlace

    def removePiece(self):
        x = self.currentPiece.x
        y = self.currentPiece.y
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0:
                    self.grid[r+y][c+x] = 0

    def updatePiece(self):
        x = self.currentPiece.x
        y = self.currentPiece.y
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0:
                    self.grid[r+y][c+x] = self.currentPiece.arrangement[r][c]

    def printGrid(self):
        for r in range(ROWS - 1, -1, -1):
            print(str(r) + str(self.grid[r]))
        print("-------------")

    def movePieceLeft(self):
        self.removePiece()
        self.currentPiece.shiftLeft()
        x = self.currentPiece.x
        y = self.currentPiece.y
        doMove = True
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0 and self.grid[r+y][c+x] != 0:
                    doMove = False
        if not doMove:
            self.currentPiece.shiftRight()
        self.updatePiece()
        return doMove

    def movePieceRight(self):
        self.removePiece()
        self.currentPiece.shiftRight()
        x = self.currentPiece.x
        y = self.currentPiece.y
        doMove = True
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0 and self.grid[r+y][c+x] != 0:
                    doMove = False
        if not doMove:
            self.currentPiece.shiftLeft()
        self.updatePiece()
        return doMove

    def movePieceDown(self):
        self.removePiece()
        self.currentPiece.fall()
        x = self.currentPiece.x
        y = self.currentPiece.y
        doMove = True
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0 and self.grid[r+y][c+x] != 0:
                    doMove = False
        if not doMove:
            self.currentPiece.rise()
            if not self.bottomReset():
                self.gameOver = True
        self.updatePiece()
        return doMove

    def rotateClockwise(self):
        self.removePiece()
        self.currentPiece.rotateClockwise()
        x = self.currentPiece.x
        y = self.currentPiece.y
        doMove = True
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0 and self.grid[r+y][c+x] != 0:
                    doMove = False
        if not doMove:
            self.currentPiece.rotateCounterClockwise()
        self.updatePiece()
        return doMove

    def rotateCounterClockwise(self):
        self.removePiece()
        self.currentPiece.rotateCounterClockwise()
        x = self.currentPiece.x
        y = self.currentPiece.y
        doMove = True
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0 and self.grid[r+y][c+x] != 0:
                    doMove = False
        if not doMove:
            self.currentPiece.rotateClockwise()
        self.updatePiece()
        return doMove

    def update(self, moveChoice): #moveChoice is a pair where 0 = clockwise, 1 = counterclockwise, 2 = no turn -> 0 = left shift, 1 = right shift, 2 = no horizontal shift
        if moveChoice % 3 == 0:
            self.rotateClockwise()
        elif moveChoice % 3 == 1:
            self.rotateCounterClockwise()
        
        if moveChoice - (moveChoice % 3) == 0:
            self.movePieceLeft()
        elif moveChoice - (moveChoice % 3) == 1:
            self.movePieceRight()

        if self.stallFrames <= 0:
            self.movePieceDown()
            self.stallFrames = FRAMES_BEFORE_FALL
        else:
            self.stallFrames -= 1

    def bottomReset(self):
        self.addPiece(self.currentPiece)
        rowsCleared = 0
        for r in range(ROWS-4, 3, -1):
            isRowComplete = True
            for c in range(3, COLUMNS - 3):
                if self.grid[r][c] == 0:
                    isRowComplete = False
                    break
            if isRowComplete:
                for r2 in range(r, ROWS - 4):
                    self.grid[r2] = list(self.grid[r2+1])   
                rowsCleared += 1
        newPiece = self.queue.getPiece()
        self.score += 1 # Potentially remove
        if rowsCleared == 1:
            self.score += 40
        elif rowsCleared == 2:
            self.score += 100
        elif rowsCleared == 3:
            self.score += 300
        elif rowsCleared == 4:
            self.score += 1200

        if not self.addPiece(newPiece):
            return False
        self.piecesPlaced += 1
        return True

    def getEnvGrid(self):
        envGrid = np.zeros(shape = (24,10), dtype = np.int32)
        for r in range(ROWS-8):
            for c in range(COLUMNS-6):
                if self.grid[r+4][c+3] > 0:
                    envGrid[r][c] = 1
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0:
                    envGrid[r+self.y-4][c+self.x-3] = 2
        return envGrid



    