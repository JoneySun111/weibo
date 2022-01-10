from mapping import *


class BaseTransform:
    def __init__(self, mapping_path, max_word_size):
        self.mp = mapping.load(mapping_path)
        self.mp.set_word_size(max_word_size)

    def __call__(self, data):
        data = self.mp.mapping_from_sentences(data)
        return data
