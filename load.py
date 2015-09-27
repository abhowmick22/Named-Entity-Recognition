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

class CoNLL2k3Loader(Loader):
    'Loader to read and write data in the CoNLL 2003 shared data format'

    def __init__(self, test_file, train_file):
        self.test_file = test_file
        self.train_file = train_file

    def get_next_test_point(self):
        pass

    # get the tokens one at a time
    def get_tokens(self, point):
        pass

    # get the tokens as windows
    def get_window_tokens(self, point):
        tokens = self.get_tokens(point)
        iterator = iter(tokens)
        prev = None
        item = iterator.next()  # throws StopIteration if empty.
        for next in iterator:
            yield (prev,item,next)
            prev = item
            item = next
        yield (prev,item,None)