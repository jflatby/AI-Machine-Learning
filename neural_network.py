import numpy as np
import random
from game import Game
from vec2d import Vec2d
import matplotlib.pyplot as plt

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.utils import to_categorical

plt.style.use("ggplot")

class NeuralNet():
    def __init__(self):
        random.seed = 13337
        self.reward = 0
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.epsilon = 0
        self.actual = []
        self.memory = []
        self.num_inputs = 1
        self.model = self.network()
        # self.model = self.network("weights.hdf5")

        self.scores = []
        self.current_game = 0

        self.game = Game(self)

    def get_state(self, player, food):
        """
        The state is defined by a single boolean, which is True or
        False depending on whether the vector from the player to the
        food is to the right or left of the current direction vector.
        """
        food_vec = food.position - player.position
        direction = Vec2d(player.direction.x, -player.direction.y)

        #right_beam = direction.rotated(45) * 50
        #left_beam = direction.rotated(-45) * 50

        #r = player.position + right_beam
        #right_collide = r.x < 0 or r.x > 800 or r.y < 0 or r.y > 600

        #l = player.position + left_beam
        #left_collide = l.x < 0 or l.x > 800 or l.y < 0 or l.y > 600

        state = [
            direction.get_angle_between(food_vec) > 0, #food is to the right/left
        ]
        #print(state)

        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0

        return np.asarray(state)

    def network(self, weights=None):
        """
        Creates the actual neural network, currently consisting of
        the input layer, one hidden layer with 120 neurons and the
        output layer containing two booleans, turn left and turn right.
        I do it this way instead of a single boolean because it leaves
        room for having both false and not turn at all.
        """
        model = Sequential()
        model.add(Dense(activation='relu', input_dim=self.num_inputs, units=120))
        model.add(Dropout(0.15))
        #model.add(Dense(activation='relu', units=120))
        #model.add(Dropout(0.15))
        #model.add(Dense(activation='relu', units=120))
        #model.add(Dropout(0.15))
        model.add(Dense(activation='softmax', units=2))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)

        return model

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, self.num_inputs)))[0])
        target_f = self.model.predict(state.reshape((1, self.num_inputs)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, self.num_inputs)), target_f, epochs=1, verbose=0)

    def advance(self, player, food):
        """
        Called from the Game class main loop each tick.
        """

        #Less randomness after more games, none after 50.
        epsilon = 50 - self.current_game

        old_state = self.get_state(player, food)

        #Perform random or predicted move based on epsilon
        if random.randint(0, 200) < epsilon:
            final_move = to_categorical(random.randint(0, 1), num_classes=2)
        else:
            prediction = self.model.predict(old_state.reshape(1, self.num_inputs))
            final_move = to_categorical(np.argmax(prediction[0]), num_classes=2)

        #Act on the chosen input
        player.perform_actions(final_move)
        player.move()
        new_state = self.get_state(player, food)

        #Get positive reward for food and negative for dying
        if player.got_point:
            reward = 10
        elif player.dead:
            reward = -10
        else:
            reward = 0

        self.train_short_memory(old_state, final_move, reward, new_state, False)

        self.memory.append((old_state, final_move, reward, new_state, False))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def print_results(self):
        plt.scatter(range(len(self.scores)), self.scores)
        plt.show()

    def main_loop(self):
        total_games = 50
        for i in range(total_games):
            self.current_game = i
            print(f"Starting game {i}..")
            self.game.simple_loop()
            self.replay_new(self.memory)

            self.scores.append(self.game.player.points)

            self.game.player.reset()
            self.game.player.dead = False

        print(self.scores)
        plt.scatter(range(total_games), self.scores)
        plt.show()

if __name__ == "__main__":
    net = NeuralNet()
    net.main_loop()
    #net.game.loop()