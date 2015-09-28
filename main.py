__author__ = 'abhishek'
#!/usr/bin/python

# This is the driver program that parses command line arguments and performs NER

import featureVecs
import featureFuncs
from load import CoNLL2k3Loader
from decoder import Viterbi
import argparse

# read the arguments
parser = argparse.ArgumentParser(description='read the arguments')
parser.add_argument('--test', help='test file')
parser.add_argument('--weights', help='weights file for the features')
parser.add_argument('--output', help='file to write outputs')
args = parser.parse_args()

# define NER classes as a dict
classes = {'0': 'B-PER', '1': 'B-LOC', '2': 'B-ORG', \
           '3': 'I-PER', '4': 'I-LOC', '5': 'I-ORG', \
           '5': 'O'}

# load 'test'
loader = CoNLL2k3Loader('dummy', args.test, args.output)
weights_fname = args.weights

# for each sentence in test, each sentence is a list of word tokens
sentence = []
loader.get_next_test_point(sentence)
while sentence is not None:
    # get window tokens from this sentence
    window_tokens = loader.get_window_tokens(sentence)
    # instantiate viterbi decoder for this sentence
    viterbi = Viterbi(len(sentence), classes, weights_fname)
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