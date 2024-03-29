from tensorflow.keras import *
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class Agent():
    def __init__(self, player):
        self.model = Sequential()
        self.model.add(layers.Dense(10, activation='relu', input_dim=22))
        self.model.add(layers.Dense(10, activation='relu'))
        self.model.add(layers.Dense(4, activation='sigmoid'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])
        self.y = 0.95
        self.eps = 0.5
        self.decay_factor = 0.9999
        self.eps_min = 0.01
        self.player = player
        self.score = self.player.score
        self.actions = self.player.actions
        self.state = []
        self.memory = []
        self.moves = [0, 0, 0, 0]

    def move(self, asteroids):
        previous_acts = []
        for act in self.actions:
            if act:
                previous_acts.append(1)
            else:
                previous_acts.append(0)
        self.state = [self.player.x,
                      self.player.y,
                      self.player.velocity_x,
                      self.player.velocity_y,
                      self.player.rotation,
                      self.player.num_lives] + previous_acts + asteroids
        if np.random.random() < self.eps:
            acts = np.random.rand(4)
        else:
            acts = self.model.predict(np.array([self.state,]))[0]
        i = 0
        for act in acts:
            if act > 0.65:
                self.actions[i] = True
            else:
                self.actions[i] = False
            if self.actions[i] == self.player.actions[i]:
                self.moves[i] = 0
            else:
                self.moves[i] = 1
            i += 1
        self.player.actions = self.actions

    def remember(self, asteroids):
        self.memory.append((self.state,
                           self.moves,
                           (self.player.score - self.score)*self.player.num_lives,
                           [self.player.x,
                           self.player.y,
                           self.player.velocity_x,
                           self.player.velocity_y,
                           self.player.rotation,
                           self.player.num_lives] + self.actions + asteroids))
        self.score = self.player.score




    def replay(self, all=False):
        if all:
            for state, action, reward, next_state in self.memory[-10:]:

                target = reward + self.y * \
                       np.amax(self.model.predict(np.array([next_state,]))[0])
                target_f = self.model.predict(np.array([state,]))
                target_f[0][action] = target
                self.model.fit(np.array([state,]), target_f, epochs=1, verbose=0)
        else:
            for state, action, reward, next_state in self.memory[-10:]:

                target = reward + self.y * \
                       np.amax(self.model.predict(np.array([next_state,]))[0])
                target_f = self.model.predict(np.array([state,]))
                target_f[0][action] = target
                self.model.fit(np.array([state,]), target_f, epochs=1, verbose=0)
        if self.eps > self.eps_min:
            self.eps *= self.decay_factor

    def save(self, name):
        self.model.save_weights('/User/eliprater/github/Asteroids/version3/game/trained_models/model_{}.h5'.format(name))
        # target = r + y * np.max(model.predict(np.array([next_state,])))
        # target_vec = self.model.predict(np.array([vars,]))
        # target_vec[a] = target
        # model.fit(np.array([vars,]), target_vec.reshape(-1, 7), epochs=1, verbose=0)
