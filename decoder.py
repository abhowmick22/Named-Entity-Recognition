__author__ = 'abhishek'
from featureVecs import FeatGenerator
import math

# This module implements the Viterbi algorithm
# use the weights to compute the score

class Viterbi:
    'Viterbi decoder to estimate the most likely sequence'

    def __init__(self, length, classes, weights, gazetteer):
        self.length = length
        self.classes = classes
        self.trellis = [[(0.0, 0) for i in range(length)] for j in range(len(classes))]
        self.weights = {}
        self.read_weights(weights, self.weights)
        self.feature_gen = FeatGenerator(gazetteer)

    def read_weights(self, weights_fname, weights_dict):
        file = open(weights_fname, 'r')
        for line in file.readlines():
            tokens = line.split()
            weights_dict[tokens[0]] = float(tokens[1])

    # this method computes the local features given a word and its context
    def get_log_local_score(self, prev_word, prev_pos_tag, curr_word, curr_pos_tag, \
                        next_word, next_pos_tag, prev_ner_tag, curr_ner_tag, token_nbr):
        feats = {}
        self.feature_gen.get_feature_vector(prev_word, prev_pos_tag, curr_word, curr_pos_tag, \
                                            next_word, next_pos_tag, prev_ner_tag, curr_ner_tag, token_nbr, feats)
        score = 0.0
        for key, value in feats.iteritems():
            increment = (value * self.weights.get(key, 0.0))
            score = score + increment
            if increment > 0.0 and curr_ner_tag is 'O':
                print key, value
        return math.log(score) if score > 0.0 else -100.0

    # computes the maximums and updates column of the trellis
    def update_trellis(self, prev, curr, next, token_nbr):
        class_indices = range(len(self.classes))
        # extract the word and pos tag from prev, curr and next
        prev_word = prev[0]
        prev_pos_tag = prev[1]
        curr_word = curr[0]
        curr_pos_tag = curr[1]
        next_word = next[0]
        next_pos_tag = next[1]
        for i in class_indices:
            max_score = 0.0
            backpointer = 0
            curr_ner_tag = self.classes[i]
            # check for STOP and START
            for j in class_indices:
                prev_ner_tag = self.classes[j]
                if token_nbr is 0:
                    prev_score = 0.0
                else:
                    prev_score = self.trellis[j][token_nbr-1][0]
                score = prev_score + self.get_log_local_score(prev_word, prev_pos_tag, curr_word, curr_pos_tag, \
                                                          next_word, next_pos_tag, prev_ner_tag, curr_ner_tag, token_nbr)
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
            result.append(self.classes[class_index])