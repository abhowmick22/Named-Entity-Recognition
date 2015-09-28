__author__ = 'abhishek'
from featureVecs import FeatGenerator

# This module implements the Viterbi algorithm
# use the weights to compute the score

class Viterbi:
    'Viterbi decoder to estimate the most likely sequence'

    def __init__(self, length, classes, weights, gazetteer):
        self.length = length
        self.classes = classes
        self.trellis = [[(0.0, 'dummy') for i in range(length)] for j in range(len(classes))]
        self.weights = {}
        self.read_weights(weights, self.weights)
        self.feature_gen = FeatGenerator(gazetteer)

    def read_weights(self, weights_fname, weights_dict):
        file = open(weights_fname, 'r')
        for line in file.readlines():
            tokens = line.split()
            weights_dict[tokens[0]] = float(tokens[1])

    # this method computes the local features given a word and its context
    def get_local_score(self, prev_word, curr_word, next_word, prev_tag, curr_tag):
        feats = {}
        self.feature_gen.get_feature_vector(prev_word, curr_word, next_word, prev_tag, curr_tag, feats)
        score = 0.0
        for key, value in feats.iteritems():
            score = score + (value * self.weights.get(key, 0.0))
        return score

    # computes the maximums and updates column of the trellis
    def update_trellis(self, prev, curr, next, token_nbr):
        class_indices = range(len(self.classes))
        for i in class_indices:
            max_score = 0.0
            backpointer = 0
            curr_tag = self.classes[i]
            # check for STOP
            for j in class_indices:
                prev_tag = self.classes[j]
                prev_score = self.trellis[j][token_nbr-1][0]
                score = prev_score * self.get_local_score(prev, curr, next, prev_tag, curr_tag)
                if score > max_score:
                    max_score = score
                    backpointer = j
            self.trellis[i][token_nbr] = (max_score, backpointer)

    def get_output_sequence(self, result):
        sequence = []
        num_classes = len(self.classes)
        bp = len(self.classes)-1
        for i in reversed(range(self.length)):
            sequence.append(bp)
            bp = self.trellis[bp][i][1]
        for class_index in reversed(sequence):
            result.add(self.classes[class_index])