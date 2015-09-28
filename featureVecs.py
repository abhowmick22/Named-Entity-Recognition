__author__ = 'abhishek'

# This module operates on the feature vectors

class FeatGenerator:
    'A module that computes the feature vectors'

    def __init__(self, gazetteer):
        self.gazetteer = gazetteer

    def get_feature_vector(self, prev_word, curr_word, next_word, prev_tag, curr_tag, features):
        pass