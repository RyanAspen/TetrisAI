#Usable columns 3-12, 0-3 rotations

from tetromino import tetromino
from tetrominoQueue import tetrominoQueue 
import numpy as np
import math
import copy

ROWS = 28
COLUMNS = 16
BOXSIZE = 30

maxPieces = 500

class gameboard:
    def __init__(self):
        self.score = 0
        self.reward = 0.0
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
        self.addingPiece = False
        self.x = 0
        self.y = 0
        self.holes = 0
        self.aggHeight = 0
        self.bumpiness = 0
        self.height = 0
        self.rowsCleared = 0

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
        for r in range(ROWS - 1, 0, -1):
            print(str(r) + ":" + str(self.grid[r]))
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
            self.addingPiece = True
            if not self.bottomReset():
                self.gameOver = True
        self.updatePiece()
        return doMove

    def fastFall(self):
        while self.movePieceDown():
            pass

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
        didMove = False
        if moveChoice[0] == 0:
            didMove = self.rotateClockwise()
        elif moveChoice[0] == 1:
            didMove = self.rotateCounterClockwise()
        
        if moveChoice[1] == 0:
            if self.movePieceLeft():
                didMove = True
        elif moveChoice[1] == 1:
            if self.movePieceRight():
                didMove = True
        return didMove

    def printGrid(self, grid):
        for r in range(27, 0, -1):
            print(str(r) + ":" + str(grid[r]))
        print("-------------")

    def updateFullMovement(self, moveChoice, saveMoves = False):
        rotations = moveChoice % 4
        column = math.floor(moveChoice / 4)
        myGrids = []
        currCol = self.currentPiece.x
        while currCol != column or rotations != 0:
            currCol = self.currentPiece.x - 3
            movement = [2,2]
            if column > currCol:
                #Right Shift
                movement[1] = 1
            elif column < currCol:
                #Left Shift
                movement[1] = 0
            if rotations == 3:
                #CounterClockwise Rotation
                movement[0] = 1
                rotations = 0
            elif rotations > 0:
                #Clockwise Rotation
                movement[0] = 0
                rotations -= 1
            didMove = self.update(movement)
            if not didMove:
                break
            if saveMoves:
                myGrids.append(copy.deepcopy(self.grid))
        self.fastFall()
        return myGrids

    def bottomReset(self):
        self.addPiece(self.currentPiece)
        self.rowsCleared = 0
        for r in range(ROWS-4, 3, -1):
            isRowComplete = True
            for c in range(3, COLUMNS - 3):
                if self.grid[r][c] == 0:
                    isRowComplete = False
                    break
            if isRowComplete:
                for r2 in range(r, ROWS - 4):
                    self.grid[r2] = list(self.grid[r2+1])   
                self.rowsCleared += 1
        aggHeight = self.getAggregateHeight()
        bumpiness = self.getBumpiness()
        holes = self.getHoles()
        rowCompleteness = self.getAvgRowCompleteness()
        oldScore = self.score
        #print(str(-0.08 * aggHeight) + " " + str(0.76 * self.rowsCleared) + " " + str(-0.36 * holes) + " " + str(-0.18 * bumpiness))
        newScore = (-0.28 * aggHeight) + (0.76 * self.rowsCleared) + (-0.36 * holes) + (-0.18 * bumpiness)
        self.reward = newScore - oldScore
        self.score = newScore    
        if sum(self.grid[24]) > 48: #Change later for cleanliness
            return False
        newPiece = self.queue.getPiece()
        self.addPiece(newPiece)
        self.piecesPlaced += 1
        if self.piecesPlaced > maxPieces:
            return False
        return True

    def getEnvGrid(self):
        envGrid = []
        for r in range(ROWS-4):
            envRow = []
            for c in range(COLUMNS-6):
                if self.grid[r+4][c+3] > 0:
                    envRow.append([1])
                else:
                    envRow.append([0])
            envGrid.append(envRow)
        for r in range(4):
            for c in range(4):
                if self.currentPiece.arrangement[r][c] != 0:
                    envGrid[r+self.y+4][c+self.x+3] = [2]
        return envGrid

    def getReward(self):
        return self.reward

    def getHeight(self, column):
        height = 0
        temp = 0
        for r in range(3, 28):
            temp += 1
            if self.grid[r][column] > 0:
                height = temp
        return height

    def getAggregateHeight(self):
        aggregateHeight = 0
        for c in range(3,13):
            aggregateHeight += self.getHeight(c)
        return aggregateHeight
    
    def getHoles(self):
        holes = 0
        for c in range(3, COLUMNS - 3):
            block = False
            for r in range(4, ROWS - 4):
                if self.grid[r][c] != 0:
                    block = True
                elif self.grid[r][c] == 0 and block:
                    holes += 1
        return holes

    def getBumpiness(self):
        bumpiness = 0
        for c in range(3, 11):
            bumpiness += abs(self.getHeight(c) - self.getHeight(c+1))
        return bumpiness

    def getAvgRowCompleteness(self):
        totalRowCompleteness = 0.0
        rowsChecked = 0
        for r in range(ROWS - 5, 3, -1):
            shouldCount = False
            rowCompleteness = 0.0
            for c in range(3, COLUMNS - 3):
                if self.grid[r][c] > 0:
                    shouldCount = True
                    rowCompleteness += 1
            if shouldCount:
                rowsChecked += 1
                totalRowCompleteness += rowCompleteness
        if rowsChecked == 0:
            return 0
        return totalRowCompleteness / rowsChecked