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

# load 'test'
loader = CoNLL2k3Loader('dummy', args.test)
weights_fname = args.weights
output_file = open(args.output,'w')

# for each sentence in test, each sentence is a list of word tokens
sentence = loader.get_next_test_point()
while sentence is not None:

    # get window tokens from this sentence
    window_tokens = loader.get_window_tokens(sentence)

    # instantiate viterbi decoder for this sentence
    viterbi = Viterbi(1, {}, weights_fname, window_tokens)

    # for each token in sentence
    token_nbr = 0
    for (prev, curr, next) in window_tokens:

        # get local scores for each class supplying current word and previous word info
        feature_vector = viterbi.get_local_features()

        # invoke viterbi to populate trellis at ith position
        viterbi.update_trellis(feature_vector, token_nbr)

    # output structure for sentence using backpointers
    output = viterbi.get_output_sequence()
    loader.write_output(output_file, output, sentence)

    # delete viterbi decoder
    del viterbi

    sentence = loader.get_next_test_point()
