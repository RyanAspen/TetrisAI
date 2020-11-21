#Not correct

import csv
class tetrominoData:
    def __init__(self):
        tetrisFile = open('TetrisData.csv', 'r')
        tdreader = csv.reader(tetrisFile, delimiter = ' ')
        self.tetrisData = []
        tempData = []
        tempState = []
        c = 0
        for row in tdreader:
            splitRow = row[0].split(",")
            splitRow = [int(i) for i in splitRow]
            tempData.append(splitRow)
            c += 1
            if c % 4 == 0:
                tempState.append(tempData)
                tempData = []
                if c % 16 == 0:
                    self.tetrisData.append(tempState)
                    tempState = []

    def getArrangement(self, shape, arrangement):
        return self.tetrisData[shape][arrangement]


