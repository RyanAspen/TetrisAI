from gameboard import gameboard
import random 

game = gameboard()
while not game.gameOver:
    r1 = random.randint(0,2)
    r2 = random.randint(0,2)
    game.update((r1,r2))
