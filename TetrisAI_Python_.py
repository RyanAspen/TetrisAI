#https://medium.com/@ashwindesilva/how-to-use-google-colaboratory-to-clone-a-github-repository-e07cf8d3d22b

# TODO
# Implement System to save training (keras Checkpoints?)
# Speed up gameboard if possible?
# Experiment with training variables

from TetrisAICollection import TetrisAICollection

collection = TetrisAICollection()
collection.validateEnv()
collection.train()