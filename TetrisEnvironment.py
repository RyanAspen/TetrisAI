from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
import tf_agents.specs as array_spec
from gameboard import gameboard
import numpy as np

class TetrisEnvironment(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int, minimum=0, maximum=51, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(24,10,1), dtype=np.int, minimum=0, maximum=2, name='observation')
        self.currentGame = gameboard()
        self._state = self.currentGame.getEnvGrid()
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.currentGame = gameboard()
        self._episode_ended = False
        self._state = self.currentGame.getEnvGrid()
        return ts.restart(np.array(self._state, dtype=np.int))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()
        if self.currentGame.gameOver:
            self._episode_ended = True
        else:
            self.currentGame.updateFullMovement(action)
            self._state = self.currentGame.getEnvGrid()
        if self._episode_ended:
            return ts.termination(np.array(self._state, dtype=np.int), self.currentGame.getReward() - 25)
        return ts.transition(np.array(self._state, dtype=np.int), self.currentGame.getReward())

class TetrisEnvironmentEval(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int, minimum=0, maximum=51, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(24,10,1), dtype=np.int, minimum=0, maximum=2, name='observation')
        self.currentGame = gameboard()
        self._state = self.currentGame.getEnvGrid()
        self._episode_ended = False
        self.score = 0
        self.grids = []

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.currentGame = gameboard()
        self.score = 0
        self._episode_ended = False
        self._state = self.currentGame.getEnvGrid()
        return ts.restart(np.array(self._state, dtype=np.int))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()
        if self.currentGame.gameOver:
            self._episode_ended = True
        else:
            self.grids = self.currentGame.updateFullMovement(action, True)
            self.score += self.currentGame.rowsCleared
            self._state = self.currentGame.getEnvGrid()
        if self._episode_ended:
            return ts.termination(np.array(self._state, dtype=np.int), self.currentGame.getReward() - 25)
        return ts.transition(np.array(self._state, dtype=np.int), self.currentGame.getReward())

    def getGrids(self):
        return self.grids