'''
Input: state s
Output: action a, as a one-hot vector
'''

import tensorflow as tf
import numpy as np
import random
import os.path
from BotTrainer import create_network
from BotTrainer import get_data

#–––––––––––––––––––––––––––––Hyperparameters––––––––––––––––––––––––––#
# File names
csv_file = 'data_set.csv'
weights_file = 'weights/model.ckpt'

# Input
map_width = 48
map_height = 48
num_chan = 7

# Output
num_acts = 5

# Reinforcement learning parameters
init_epsilon = 1.0
fin_epsilon = 0.05
explore = 500


class DecisionMaker():
    def __init__(self):
        self.q_s, self.s = create_network()
        self.is_weights = False

        # Load weight
        if os.path.isfile(weights_file):
            with tf.Session() as sess:
                saver = tf.train.Saver()
                saver.restore(sess, "weights/model.ckpt")
            print('Weights loaded')
        else:
            self.is_weights = True
            # Initialisation
            init = tf.global_variables_initializer()

            # Session
            self.sess = tf.Session()
            self.sess.run(init)
            print('initialised')

    def make_decision(self, s_in):
        # action one-hot vector
        a = np.zeros(num_acts)

        s_in = np.reshape(s_in, (1, map_width, map_height, num_chan))

        # Move randomly if first time, else move according to learnt strategy
        if not self.is_weights:
            a_index = random.randrange(num_acts)
            a[a_index] = 1
            return a

        else:
            # epsilon to make sure further learning
            epsilon = init_epsilon

            # decide whether to explore or stick to the best known strategy
            if random.random() <= epsilon:
                a_index = random.randrange(num_acts)
            else:
                # TODO: Is this right?
                # scale down epsilon
                if epsilon > fin_epsilon:
                    epsilon -= (init_epsilon - fin_epsilon) / explore

                with self.sess:
                    q = self.q_s.eval(feed_dict={self.s: s_in})
                a_index = np.argmax(q)

            a[a_index] = 1
            return a


batches = get_data()

dec = DecisionMaker()
a = dec.make_decision(batches[0][0][0])
print(a)

