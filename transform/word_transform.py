# from mapping import *


class WordTransfomer:
    # def __init__(self, max_word_size):
    #     self.max_word_size = max_word_size

    def __call__(self, data):
        data = list(map(lambda x: eval(x), data))
        # data = list(
        #     map(
        #         lambda x: x[:self.max_word_size]
        #         + [mapping.UNK_TAG]
        #         * (self.max_word_size - len(x) if self.max_word_size - len(x) > 0 else 0),
        #         data,
        #     )
        # )
        return data
