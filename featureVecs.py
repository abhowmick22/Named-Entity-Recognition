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

    def get_feature_vector(self, prev, curr, next, prev_ner_tag, curr_ner_tag, token_nbr, features):
        # extract the word and pos tag from prev, curr and next
        prev_word = prev[0]
        prev_pos_tag = prev[1]
        curr_word = curr[0]
        curr_pos_tag = curr[1]
        next_word = next[0]
        next_pos_tag = next[1]

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
        feature_keys.append('Pi-1=' + prev_pos_tag + ner_tag_suffix)
        feature_keys.append('Wi+1=' + next_word + ner_tag_suffix)
        feature_keys.append('Pi+1=' + next_pos_tag + ner_tag_suffix)
        # we don't really need equivalents of features 2 and 4
        # change feature 7 if you add 2 or 4

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
        for i in range(8):
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


        for key in feature_keys:
            features[key] = 1.0




    def get_shape(self, word):
        return "".join(['A' if c.isupper() else 'a' for c in word])
