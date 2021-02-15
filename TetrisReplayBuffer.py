import numpy as np
import random
from collections import deque

class TetrisReplayBuffer:

    def __init__(self, batch_size):
        self.gameplay_experiences = deque(maxlen = 1000000)
        self.batch_size = batch_size

    def getLength(self):
        return len(self.gameplay_experiences)

    def store_gameplay_experience(self, state, next_state, reward, action, done):
        self.gameplay_experiences.append((state, next_state, reward, action, done))

    def sample_gameplay_batch(self):
        sampled_gameplay_batch = random.sample(self.gameplay_experiences, self.batch_size)
        state_batch, next_state_batch, action_batch, reward_batch, done_batch = [], [], [], [], []
        for gameplay_experience in sampled_gameplay_batch:
            state_batch.append(gameplay_experience[0])
            next_state_batch.append(gameplay_experience[1])
            reward_batch.append(gameplay_experience[2])
            action_batch.append(gameplay_experience[3])
            done_batch.append(gameplay_experience[4])
        return np.array(state_batch), np.array(next_state_batch), action_batch, reward_batch, done_batch

