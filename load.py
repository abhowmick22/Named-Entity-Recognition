__author__ = 'abhishek'
from abc import ABCMeta, abstractmethod

# Module to load data from different formats

class Loader(object):
    'General loader class'
    __metaclass__ = ABCMeta

    # return next test instance
    @abstractmethod
    def get_next_test_point(self):
        pass

    # return list of tokens given an instance
    @abstractmethod
    def get_tokens(self, point):
        pass

    # method to write the output
    @abstractmethod
    def write_output(self, output, sentence):
        pass

class CoNLL2k3Loader(Loader):
    'Loader to read and write data in the CoNLL 2003 shared data format'

    def __init__(self, train_file, test_file, output_file):
        if train_file is not 'dummy':
            self.train_file = open(train_file, 'r')
        if test_file is not 'dummy':
            self.test_file = open(test_file, 'r')
        if output_file is not 'dummy':
            self.output_file = open(output_file, 'w')

    def get_next_test_point(self, sentence):
        token = self.test_file.readline().strip()
        if not token:
            return None
        while token:
            sentence.append(token)
            token = self.test_file.readline().strip()

    # get the tokens one at a time
    def get_tokens(self, point, result):
        for p in point:
            result.append(tuple(p.split()))

    # get the tokens as windows
    def get_window_tokens(self, point):
        tokens = []
        self.get_tokens(point, tokens)
        iterator = iter(tokens)
        prev = ('<START>', '<START>', '<START>', '<START>')
        item = iterator.next()  # throws StopIteration if empty.
        for next in iterator:
            yield (prev,item,next)
            prev = item
            item = next
        yield (prev,item,('<STOP>', '<STOP>', '<STOP>', '<STOP>'))

    # method to write the output
    def write_output(self, output, sentence):
        pairs = zip(output, sentence)
        for op, token in pairs:
            self.output_file.write(token + ' ' + op + '\n')
        self.output_file.write('\n')
        self.output_file.flush()