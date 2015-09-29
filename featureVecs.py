__author__ = 'abhishek'

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

        ner_tag_suffix = ':Ti=' + curr_ner_tag
        feature_keys = []
        # feature 1
        feature_keys.append('Wi=' + curr_word + ner_tag_suffix)

        # feature 2
        feature_keys.append('Oi=' + curr_word.lower() + ner_tag_suffix)

        # feature 3
        feature_keys.append('Pi=' + curr_pos_tag + ner_tag_suffix)

        # feature 4
        feature_keys.append('Si=' + self.get_shape(curr_word) + ner_tag_suffix)

        # feature 5
        feature_keys.append('Wi-1=' + prev_word + ner_tag_suffix)
        if prev_word is not '<START>':
            feature_keys.append('Oi-1=' + prev_word.lower() + ner_tag_suffix)
            feature_keys.append('Si-1=' + self.get_shape(prev_word) + ner_tag_suffix)
        feature_keys.append('Pi-1=' + prev_pos_tag + ner_tag_suffix)
        feature_keys.append('Wi+1=' + next_word + ner_tag_suffix)
        if next_word is not '<STOP>':
            feature_keys.append('Oi+1=' + next_word.lower() + ner_tag_suffix)
            feature_keys.append('Si+1=' + self.get_shape(next_word) + ner_tag_suffix)
        feature_keys.append('Pi+1=' + next_pos_tag + ner_tag_suffix)
        # change feature 7 if you add 2 or 4
        features_type1to5 = len(feature_keys)       # will be useful for feature of type 7

        # feature 6
        for i in range(4):
            part = feature_keys[i].split(':')[0]
            feature_keys.append(part + ':Wi-1=' + prev_word + ner_tag_suffix)
            feature_keys.append(part + ':Pi-1=' + prev_pos_tag + ner_tag_suffix)
            feature_keys.append(part + ':Wi+1=' + next_word + ner_tag_suffix)
            feature_keys.append(part + ':Pi+1=' + next_pos_tag + ner_tag_suffix)

        # feature 7
        part = 'Ti-1=' + prev_ner_tag + ner_tag_suffix
        feature_keys.append(part)
        for i in range(features_type1to5):
            feature_keys.append(feature_keys[i].split(':')[0] + ':' + part)

        # feature 8
        for i in range(min(len(curr_word), 4)):
            feature_keys.append('PREi=' + curr_word[:i+1] + ner_tag_suffix)

        # feature 9
        if curr_ner_tag is not 'O':
            tag = curr_ner_tag.split('-')[1]
            if self.gazetteer.get(curr_word, '') is tag:
                feature_keys.append('GAZi=True' + ner_tag_suffix)

        # feature 10
        if curr_word[0].isupper():
            feature_keys.append('CAPi=True' + ner_tag_suffix)

        # feature 11
        feature_keys.append('POSi=' + str(token_nbr+1) + ner_tag_suffix)

        # build feature vector
        for key in feature_keys:
            features[key] = 1.0


    def get_shape(self, word):
        return "".join(['A' if c.isupper() else 'a' for c in word])
