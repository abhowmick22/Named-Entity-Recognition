__author__ = 'abhishek'

# This is the driver program that parses command line arguments and performs NER

import featureVecs
from load import CoNLL2k3Loader
from decoder import Viterbi
import argparse

# read the arguments
parser = argparse.ArgumentParser(description='read the arguments')
parser.add_argument('--test', help='test file')
parser.add_argument('--weights', help='weights file for the features')
parser.add_argument('--gazetteer', help='gazetteer file')
parser.add_argument('--output', help='file to write outputs')
args = parser.parse_args()

# define 9 NER classes as a dict
classes = {0: 'B-LOC', 1: 'B-MISC', 2: 'B-ORG', 3: 'B-PER', \
           4: 'I-LOC', 5: 'I-MISC', 6: 'I-ORG', 7: 'I-PER', \
           8: 'O'}

# load 'test'
loader = CoNLL2k3Loader('dummy', args.test, args.output)
weights_fname = args.weights
gazetteer = args.gazetteer

# for each sentence in test, each sentence is a list of word tokens
sentence = []
loader.get_next_test_point(sentence)
while sentence is not None:
    # get window tokens from this sentence
    window_tokens = loader.get_window_tokens(sentence)
    # instantiate viterbi decoder for this sentence
    viterbi = Viterbi(len(sentence), classes, weights_fname, gazetteer)
    # for each token in sentence
    token_nbr = 0
    for (prev, curr, next) in window_tokens:
        # get local scores for each class supplying current word and previous word info
        #feature_vector = viterbi.get_local_features(prev, curr, next)
        # invoke viterbi to populate trellis at ith position
        viterbi.update_trellis(prev, curr, next, token_nbr)
        token_nbr = token_nbr + 1
    # output structure for sentence using backpointers
    output = []
    viterbi.get_output_sequence(output)
    loader.write_output(output, sentence)

    # delete viterbi decoder
    del viterbi

    sentence = []
    loader.get_next_test_point(sentence)