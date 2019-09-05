from collections import deque
import pickle
from keras.models import Sequential
from keras.layers import Dense, Convolution2D, Flatten
from keras.optimizers import Adam
from keras import backend
import keras.models
import random
import numpy as np
from keras.regularizers import l2
import time


class ConvDQNAgent:
    def __init__(self, state_size, action_size, use_pretrained=False, pretrained_model_name=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999
        self.learning_rate = 0.00025
        self.l2_lambda = 0.0001
        self.target_model = None
        self.target_model_available = False
        if use_pretrained:
            self.load_target(pretrained_model_name)
            self.load_pretrained(pretrained_model_name)
            self.epsilon = 0.1  # exploration rate
        else:
            self.model = self._build_model()

    def huber_loss(self, a, b, in_keras=True):
        error = a - b
        quadratic_term = error * error / 2
        linear_term = abs(error) - 1 / 2
        use_linear_term = (abs(error) > 1.0)
        if in_keras:
            # Keras won't let us multiply floats by booleans, so we explicitly cast the booleans to floats
            use_linear_term = backend.cast(use_linear_term, 'float32')
        return use_linear_term * linear_term + (1 - use_linear_term) * quadratic_term

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Convolution2D(16, 8, 8, subsample=(4, 4), border_mode='same',
                                input_shape=(self.state_size[0], self.state_size[1], self.state_size[2]),
                                activation='relu', kernel_initializer='glorot_uniform', kernel_regularizer=l2(self.l2_lambda)))
        model.add(Convolution2D(32, 4, 4, subsample=(2, 2), border_mode='same', activation='relu', kernel_initializer='glorot_uniform', kernel_regularizer=l2(self.l2_lambda)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu', kernel_initializer='glorot_uniform', kernel_regularizer=l2(self.l2_lambda)))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self.huber_loss,
                      optimizer=Adam(lr=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        if self.target_model_available:
            act_values = self.target_model.predict(state)
        else:
            act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if self.target_model_available:
                if not done:
                    target = (reward + self.gamma *
                              np.amax(self.target_model.predict(next_state)[0]))
                target_f = self.target_model.predict(state)
                target_f[0][action] = target
            else:
                if not done:
                    target = (reward + self.gamma *
                              np.amax(self.model.predict(next_state)[0]))
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load_target(self, name):
        #self.target_model = keras.models.load_model(name, custom_objects={'huber_loss': self.huber_loss})
        # Architecture
        with open(name+".json", "r") as f:
            json_str = f.read()
        f.close()
        self.target_model = keras.models.model_from_json(json_str)

        # Weights
        self.target_model.load_weights(name+".h5")
        self.target_model_available = True

    def load_pretrained(self,name):
        with open(name + ".json", "r") as f:
            json_str = f.read()
        f.close()
        self.model = keras.models.model_from_json(json_str)
        # Weights
        self.model.load_weights(name + ".h5")

    def save(self, name):
        #save_time = time.strftime("%Y%m%d_%H%M")
        with open(name + ".json", "w") as f:
            f.write(self.model.to_json())
        f.close()
        # Weights
        self.model.save_weights(name+".h5")

    def save_memory(self, name):
        filehandler = open(name + "-memory.pkl", 'wb')
        pickle.dump(self.memory, filehandler, protocol=4)
        filehandler.close()

    def load_memory(self, name):
        filehandler = open(name + "-memory.pkl", 'rb')
        self.memory = pickle.load(filehandler)

		