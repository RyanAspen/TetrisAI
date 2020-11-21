from tetrominoData import tetrominoData

data = tetrominoData()

class tetromino:
    
    def __init__(self, shapeId, arrangementId, x, y):
        self.x = x
        self.y = y
        self.shapeId = shapeId
        self.arrangementId = arrangementId
        self.arrangement = data.getArrangement(shapeId, arrangementId)

    def rotateClockwise(self):
        self.arrangementId = (self.arrangementId + 1) % 4
        self.arrangement = data.getArrangement(self.shapeId, self.arrangementId)

    def rotateCounterClockwise(self):
        if (self.arrangementId == 0):
            self.arrangementId = 3
        else:
            self.arrangementId = self.arrangementId - 1
        self.arrangement = data.getArrangement(self.shapeId, self.arrangementId)

    def shiftLeft(self):
        self.x = self.x - 1

    def shiftRight(self):
        self.x = self.x + 1

    def fall(self):
        self.y = self.y - 1

    def rise(self):
        self.y = self.y + 1

