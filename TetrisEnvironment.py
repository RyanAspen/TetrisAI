from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.trajectories import time_step as ts
import tf_agents.specs as array_spec
from gameboard import gameboard
import math
import numpy

rewardScore = 30000

class TetrisEnvironment(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=numpy.int32, minimum=0, maximum=8, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(24,10), dtype=numpy.int32, minimum=0, maximum=2, name='observation')
        self.currentGame = gameboard()
        self._state = self.currentGame.getEnvGrid()
        self._episode_ended = False

    def getReward(self):
        unscaledScore = self.currentGame.score
        scaledScore = (2 / math.pi) * math.atan(unscaledScore - rewardScore)
        return scaledScore

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.currentGame = gameboard()
        self._episode_ended = False
        self._state = self.currentGame.getEnvGrid()
        return ts.restart(numpy.array(self._state, dtype=numpy.int32))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()
        self.currentGame.update(action)
        self._state = self.currentGame.getEnvGrid()
        if self.currentGame.gameOver:
            self._episode_ended = True
            return ts.termination(self._state, self.getReward())
        return ts.transition(self._state, reward = 0.0, discount=1.0)