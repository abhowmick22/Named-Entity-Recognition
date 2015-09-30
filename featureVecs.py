__author__ = 'abhishek'
import re

# This module operates on the feature vectors

class FeatGenerator:
    'A module that computes the feature vectors'

    def __init__(self, gazetteer):
        f = open(gazetteer, 'r')
        self.gazetteer = {}
        for line in f.readlines():
            tokens = line.split()
            self.gazetteer[tokens[1]] = tokens[0]

    def get_feature_vector(self, prev_word, prev_pos_tag, curr_word, curr_pos_tag, \
                           next_word, next_pos_tag, prev_ner_tag, curr_ner_tag, token_nbr, features):
        if prev_word == '<START>':
            prev_ner_tag = prev_word

        ner_tag_suffix = ':Ti=' + curr_ner_tag
        feature_keys = set()
        # feature 1
        feature_keys.add('Wi=' + curr_word + ner_tag_suffix)

        # feature 2
        feature_keys.add('Oi=' + curr_word.lower() + ner_tag_suffix)

        # feature 3
        feature_keys.add('Pi=' + curr_pos_tag + ner_tag_suffix)

        # feature 4
        feature_keys.add('Si=' + self.get_shape(curr_word) + ner_tag_suffix)

        # feature 5
        feature_keys.add('Wi-1=' + prev_word + ner_tag_suffix)
        if prev_word == '<START>':
            feature_keys.add('Oi-1=<START>' + ner_tag_suffix)
        else:
            feature_keys.add('Oi-1=' + prev_word.lower() + ner_tag_suffix)
        feature_keys.add('Si-1=' + self.get_shape(prev_word) + ner_tag_suffix)
        feature_keys.add('Pi-1=' + prev_pos_tag + ner_tag_suffix)
        feature_keys.add('Wi+1=' + next_word + ner_tag_suffix)
        if next_word == '<STOP>':
            feature_keys.add('Oi+1=<STOP>' + ner_tag_suffix)
        else:
            feature_keys.add('Oi+1=' + next_word.lower() + ner_tag_suffix)
        feature_keys.add('Si+1=' + self.get_shape(next_word) + ner_tag_suffix)
        feature_keys.add('Pi+1=' + next_pos_tag + ner_tag_suffix)
        # change feature 7 if you add 2 or 4
        #features_type1to5 = len(feature_keys)       # will be useful for feature of type 7
        features_type1to5 = set(feature_keys)

        # feature 6
        parts = ['Wi=' + curr_word, \
                 'Oi=' + curr_word.lower(), \
                 'Pi=' + curr_pos_tag, \
                 'Si=' + self.get_shape(curr_word)]
        for part in parts:
            feature_keys.add(part + ':Wi-1=' + prev_word + ner_tag_suffix)
            feature_keys.add(part + ':Pi-1=' + prev_pos_tag + ner_tag_suffix)
            feature_keys.add(part + ':Si-1=' + self.get_shape(prev_word) + ner_tag_suffix)
            if prev_word == '<START>':
                feature_keys.add(part + ':Oi-1=<START>' + ner_tag_suffix)
            else:
                feature_keys.add(part + ':Oi-1=' + prev_word.lower() + ner_tag_suffix)
            feature_keys.add(part + ':Wi+1=' + next_word + ner_tag_suffix)
            feature_keys.add(part + ':Pi+1=' + next_pos_tag + ner_tag_suffix)
            feature_keys.add(part + ':Si+1=' + self.get_shape(next_word) + ner_tag_suffix)
            if next_word == '<STOP>':
                feature_keys.add(part + ':Oi+1=<STOP>' + ner_tag_suffix)
            else:
                feature_keys.add(part + ':Oi+1=' + next_word.lower() + ner_tag_suffix)

        # feature 7
        part = 'Ti-1=' + prev_ner_tag + ner_tag_suffix
        feature_keys.add(part)
        for f in features_type1to5:
            feature_keys.add(f.rsplit(':', 1)[0] + ':' + part)

        # feature 8
        for i in range(min(len(curr_word), 4)):
            feature_keys.add('PREi=' + curr_word[:i+1] + ner_tag_suffix)

        # feature 9
        if curr_ner_tag != 'O' and self.gazetteer.get(curr_word, '') == curr_ner_tag.split('-')[1]:
            feature_keys.add('GAZi=True' + ner_tag_suffix)
        else:
            feature_keys.add('GAZi=False' + ner_tag_suffix)

        # feature 10
        if curr_word[0].isupper():
            feature_keys.add('CAPi=True' + ner_tag_suffix)
        else:
            feature_keys.add('CAPi=False' + ner_tag_suffix)

        # feature 11
        feature_keys.add('POSi=' + str(token_nbr+1) + ner_tag_suffix)

        # build feature vector
        for key in feature_keys:
            if key in features:
                features[key] = features[key] + 1.0
            else:
                features[key] = 1.0
            #if features[key] >= 1.0:
                #print key, features[key], 'greater'


    # add handling for start and stop
    def get_shape(self, word):
        if word == '<START>' or word == '<STOP>' or not self.reg_string(word):
            return word
        else:
            return "".join(['A' if c.isupper() else 'a' for c in word])

    def reg_string(self, word):
        reg=re.compile('^[A-Za-z]+$')
        return reg.match(word)