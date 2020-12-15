#https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial

from TetrisEnvironment import TetrisEnvironment

import base64
import imageio
import IPython
import matplotlib
import matplotlib.pyplot as plt
import PIL.Image
import pyvirtualdisplay

import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.environments import utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

import numpy as np

num_iterations = 20000 # @param {type:"integer"}

initial_collect_steps = 100  # @param {type:"integer"} 
collect_steps_per_iteration = 1  # @param {type:"integer"}
replay_buffer_max_length = 100000  # @param {type:"integer"}

batch_size = 64  # @param {type:"integer"}
learning_rate = 0.001  # @param {type:"number"}
log_interval = 200  # @param {type:"integer"}

num_eval_episodes = 10  # @param {type:"integer"}
eval_interval = 1000  # @param {type:"integer"}

class TetrisAICollection:

    def __init__(self):
        self.train_env = tf_py_environment.TFPyEnvironment(TetrisEnvironment())
        self.eval_env = tf_py_environment.TFPyEnvironment(TetrisEnvironment())
        self.agent = self.initAgent()
        self.replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(self.agent.collect_data_spec, self.train_env.batch_size, replay_buffer_max_length)

    def validateEnv(self):
        utils.validate_py_environment(TetrisEnvironment(), episodes=5)

    def getPolicy(self):
        return self.agent.policy

    def getCollectPolicy(self):
        return self.agent.collect_policy

    def initAgent(self):
        fc_layer_params = (100,)
        q_net = q_network.QNetwork(
            self.train_env.observation_spec(),
            self.train_env.action_spec(),
            fc_layer_params=fc_layer_params
        )
        optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
        train_step_counter = tf.Variable(0)
        agent = dqn_agent.DqnAgent(
            self.train_env.time_step_spec(),
            self.train_env.action_spec(),
            q_network=q_net,
            optimizer=optimizer,
            td_errors_loss_fn=common.element_wise_squared_loss,
            train_step_counter=train_step_counter
        )
        agent.initialize()
        return agent

    #env = eval_env, pol = agent.policy, num = num_eval_episodes
    def compute_avg_return(self, num_episodes = 10):
        total_return = 0.0
        for _ in range(num_eval_episodes):
            time_step = self.eval_env.reset()
            episode_return = 0.0
            while not time_step.is_last():
                action_step = self.agent.policy.action(time_step)
                time_step = self.eval_env.step(action_step.action)
                episode_return += time_step.reward
            total_return += episode_return
        avg_return = total_return / num_episodes
        return avg_return.numpy()[0]

    #env = train_env, pol = collect_policy, buf = replay buffer
    def collect_step(self):
      time_step = self.train_env.current_time_step()
      action_step = self.agent.getCollectPolicy().action(time_step)
      next_time_step = self.train_env.step(action_step.action)
      traj = trajectory.from_transition(time_step, action_step, next_time_step)

      # Add trajectory to the replay buffer
      self.replay_buffer.add_batch(traj)

    def collect_data(self, steps):
      for _ in range(steps):
        collect_step()

    def train(self):
        # (Optional) Optimize by wrapping some of the code in a graph using TF function.
        self.agent.train = common.function(self.agent.train)

        # Reset the train step
        self.agent.train_step_counter.assign(0)

        # Evaluate the agent's policy once before training.
        avg_return = self.compute_avg_return()
        returns = [avg_return]

        for _ in range(num_iterations):

          # Collect a few steps using collect_policy and save to the replay buffer.
          collect_data(collect_steps_per_iteration)

          # Sample a batch of data from the buffer and update the agent's network.
          experience, unused_info = next(iterator)
          train_loss = self.agent.train(experience).loss

          step = agent.train_step_counter.numpy()

          if step % log_interval == 0:
            print('step = {0}: loss = {1}'.format(step, train_loss))

          if step % eval_interval == 0:
            avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
            print('step = {0}: Average Return = {1}'.format(step, avg_return))
            returns.append(avg_return)
