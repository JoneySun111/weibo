import torch


class NgramTransfomer:
    def __init__(self, context_size):
        self.context_size = context_size

    def __call__(self, sentence):
        data = []
        label = []
        for i in range(self.context_size, len(sentence)):
            data.append(sentence[i - self.context_size : i])
            label.append(sentence[i])
        return data, label
