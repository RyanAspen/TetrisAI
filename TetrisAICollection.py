# No errors, fix envGrid, examine long-term output

# Initialization: Random
# Actions: Grouped
# Rewards: Heuristic
# Sampling: Random
# Add a decaying epsilon greedy value

from TetrisEnvironment import TetrisEnvironment
from TetrisEnvironment import TetrisEnvironmentEval
from TetrisReplayBuffer import TetrisReplayBuffer
from TetrisAgent import TetrisAgent
import matplotlib.pyplot as plt
import numpy as np
import cv2

random_iterations = 0
num_iterations = 1000000
update_interval = 100
log_interval = 500 
eval_interval = 2500 
graph_interval = 10000
video_interval = 10000
save_interval = 10000

batch_size = 32
gamma = 0.95

colors = ((255,255,255), (19,173,255), (19,46,203), (253,111,22), (94,206,28), (191,39,150), (246,12,54), (255,195,46), (0,0,0))

class TetrisAICollection:

    def __init__(self):
        self.env = TetrisEnvironment()
        self.eval_env = TetrisEnvironmentEval()
        self.agent = TetrisAgent(gamma=gamma, batch_size=batch_size)
        self.buffer = TetrisReplayBuffer(batch_size)

    def collect_gameplay_experience(self, random=False):
        state = self.env.reset().observation
        done = 1
        while done != 2:
            if random:
                 action = np.random.randint(0, 52)
            else:
                action = self.agent.collect_policy(state)
            done, reward, _, next_state  = self.env.step(action)
            self.buffer.store_gameplay_experience(state, next_state, reward, action, done)
            state = next_state
           
    def evaluate_training_result(self, num_of_episodes = 10):
        total_reward = 0.0
        total_score = 0.0
        for i in range(num_of_episodes): # Play 10 episode and take the average
            state = self.eval_env.reset().observation
            done = 1
            episode_reward = 0.0
            while done != 2:
                action = self.agent.collect_policy(state)
                done, reward, _, next_state = self.eval_env.step(action)
                episode_reward += reward
                state = next_state
            total_reward += episode_reward
            total_score += self.eval_env.score
        average_reward = total_reward / num_of_episodes
        average_score = total_score / num_of_episodes
        return average_reward, average_score

    def rgbGrid(self, grid):
        npGrid = np.zeros((240,100,3), dtype = np.uint8)
        for r in range(len(grid)-4):
            for c in range(len(grid[r])-6):
                gridNum = grid[27-r][c+3] #Flip this
                currColor = colors[gridNum]
                for a in range(10):
                    for b in range(10):
                        npGrid[(r*10)+a][(c*10)+b] = currColor
        return npGrid

    #Doesn't write anything, file is 0KB
    def create_video(self, step):
        fileName = 'TetrisStep' + str(step) + '.avi'
        writer = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(*'MJPG'), 3, (100,240))
        state = self.eval_env.reset().observation
        writer.write(self.rgbGrid(self.eval_env.currentGame.grid))
        done = 1
        while done != 2:
            action = self.agent.collect_policy(state)
            done, reward, _, next_state = self.eval_env.step(action)
            for grid in self.eval_env.getGrids():
                writer.write(self.rgbGrid(grid))
        writer.release()    

    def train_model(self):
        print("Beginning Random Iterations")
        for episode_count in range(1, random_iterations + 1):
            while self.buffer.getLength() < batch_size:
                self.collect_gameplay_experience(random=True)
            gameplay_experience_batch = self.buffer.sample_gameplay_batch()
            loss = self.agent.train(gameplay_experience_batch)
            if episode_count % update_interval == 0:
                self.agent.update_target_network()
            if episode_count % log_interval == 0:
                print("Random Step: " + str(episode_count))
        self.agent.save_model()
        print("Begin Training")
        avg_reward, avg_score = self.evaluate_training_result()
        returns = [avg_score]
        rewards = [avg_reward]
        self.create_video(0)
        print('step = 0: Average Return = {0}, Average Reward = {1}'.format(avg_score, avg_reward))
        for episode_count in range(1, num_iterations + 1):
            while self.buffer.getLength() < batch_size:
                self.collect_gameplay_experience()
            gameplay_experience_batch = self.buffer.sample_gameplay_batch()
            loss = self.agent.train(gameplay_experience_batch)
            if episode_count % update_interval == 0:
                self.agent.update_target_network()
            if episode_count % log_interval == 0:
                print("Step: " + str(episode_count))
            if episode_count % eval_interval == 0:
                avg_reward, avg_score = self.evaluate_training_result()
                print('step = {0}: Average Return = {1}, Average Reward = {2}'.format(episode_count, avg_score, avg_reward))
                returns.append(avg_score)
                rewards.append(avg_reward)
            if episode_count % graph_interval == 0:
                iterations = range(len(returns))
                iterations = [a * eval_interval for a in iterations]
                plt.plot(iterations, returns)
                plt.ylabel('Average Return')
                plt.xlabel('Iterations')
                plt.show()
                iterations = range(len(returns))
                iterations = [a * eval_interval for a in iterations]
                plt.plot(iterations, rewards)
                plt.ylabel('Average Reward')
                plt.xlabel('Iterations')
                plt.show()
            if episode_count % video_interval == 0:
                self.create_video(episode_count)
            if episode_count % save_interval == 0:
                self.agent.save_model()