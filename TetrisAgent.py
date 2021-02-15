import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import schedules 
import numpy as np
import cv2
from tensorflow.keras import initializers

#Fix checkpointing/model saving

class TetrisAgent:

    def __init__(self, gamma, batch_size, model_dir = 'tmp/models'):
        self.batch_size = batch_size
        self.q_net = self.build_dqn_model()
        self.target_q_net = self.build_dqn_model()
        self.gamma = gamma     
        self.model_dir = model_dir
        self.checkpoint_path = "training_1/cp.ckpt"
        self.model_checkpoint = tf.keras.callbacks.ModelCheckpoint(self.checkpoint_path, save_weights_only=True)
        #self.load_checkpoint()
        #self.load_model()

    def load_checkpoint(self):
        self.q_net.load_weights(self.checkpoint_path)

    def save_model(self):
        self.q_net.save(self.model_dir)

    def load_model(self):
        self.q_net = tf.keras.models.load_model(self.model_dir)

    def build_dqn_model(self):
        q_net = keras.Sequential()
        q_net.add(layers.Input(shape=(24, 10, 1), batch_size=self.batch_size))
        q_net.add(layers.Conv2D(32, 5, activation="relu", kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05), bias_initializer=initializers.Zeros()))
        q_net.add(layers.Conv2D(32, 5, activation="relu", kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05), bias_initializer=initializers.Zeros()))
        q_net.add(layers.Flatten())
        q_net.add(layers.Dense(100, activation="relu", kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05), bias_initializer=initializers.Zeros()))
        q_net.add(layers.Dense(100, activation="relu", kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05), bias_initializer=initializers.Zeros()))
        q_net.add(layers.Dense(52, activation="linear", kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05), bias_initializer=initializers.Zeros()))
        learningRateSchedule = schedules.PolynomialDecay(2e-6,10000,5e-7, power = 0.5)
        self.optimizer = keras.optimizers.RMSprop(learning_rate=learningRateSchedule)
        self.loss_fn = keras.losses.Huber()
        q_net.compile(optimizer = self.optimizer, loss=self.loss_fn)
        return q_net

    def update_target_network(self):
        self.target_q_net.set_weights(self.q_net.get_weights())


    def policy(self, state):
        state_input = tf.convert_to_tensor(state[None, :], dtype=tf.float32)
        action_q = self.q_net(state_input)
        action = np.argmax(action_q.numpy()[0], axis=0)
        return action

    def collect_policy(self, state):
        if np.random.random() > self.gamma:
            return np.random.randint(0, 52)
        return self.policy(state)

    def train(self, batch):
        state_batch, next_state_batch, action_batch, reward_batch, done_batch = batch
        current_q = self.q_net(state_batch)
        target_q = np.copy(current_q)
        next_q = self.target_q_net(next_state_batch)
        max_next_q = np.amax(next_q, axis=1)
        for i in range(state_batch.shape[0]):
            target_q[i][action_batch[i]] = reward_batch[i] if done_batch[i] else reward_batch[i] + 0.95 * max_next_q[i]
        result = self.q_net.fit(x=state_batch, y=target_q, verbose=0,callbacks=[self.model_checkpoint])
        return result.history['loss']

