from tetromino import tetromino
import random
from collections import deque

class tetrominoQueue:
    def __init__(self):
        self.queue = deque()
        self.generatePieces()

    def generatePieces(self):
        pieceIds = list()
        for a in range(7):
            pieceIds.append(a)
        random.shuffle(pieceIds)
        for piece in pieceIds:
            self.queue.append(tetromino(piece,0,8,24))

    def getPiece(self):
        piece = self.queue.popleft()
        if len(self.queue) < 5:
            self.generatePieces()
        return piece

