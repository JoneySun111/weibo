from mapping import *


class BaseTransform:
    def __init__(self, mapping_path, max_word_size = None):
        self.mp = mapping.load(mapping_path)
        if max_word_size is not None:
            self.mp.set_word_size(max_word_size)

    def __call__(self, data, mode='sentences'):
        if mode == 'sentences':
            data = self.mp.mapping_from_sentences(data)
        elif mode == 'sentence':
            data = self.mp.mapping_from_sentence(data)
        else:
            data = self.mp.word_to_id(data)
        return data

    def mapping_from_sentence(self, data):
        data = self.mp.mapping_from_sentence(data)
        return data
