__author__ = 'abhishek'

# This module implements the Viterbi algorithm
# use the weights to compute the score

class Viterbi:
    'Viterbi decoder to estimate the most likely sequence'

    def __init__(self, length, classes, weights, tokens):
        self.length = length
        self.classes = classes
        self.weights = weights
        self.tokens = tokens






