import random
from dataloader.dataloader import *
from transform.ngram_transfomer import *
from transform.base_tokenizer import *


class NgramDataloader(Dataloader):
    def __init__(self, path_list, batch_size=1, context_size=3, shuffle=True, tokenize=True):
        super().__init__(path_list, batch_size, shuffle)
        self.context_size = context_size
        self.tokenize = tokenize
        self.transfomer = NgramTransfomer(self.context_size)
        if tokenize:
            self.tokenizer = BaseTokenizer()
        else:
            self.tokenizer = None

    def reset(
        self,
    ):
        self.epoch_count += 1
        random.seed(123356 + self.epoch_count)
        if self.shuffle:
            random.shuffle(self.path_list)
        self.index = 0
        self.data = []
        for path in self.path_list:
            with open(path, 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                    line = line.replace('\u200b', '').strip().split(',')
                    # label = int(line[1])
                    input = ','.join(line[2:])
                    if self.tokenize:
                        input = self.tokenizer(input)
                    for _input, _label in list(zip(*self.transfomer(input))):
                        self.data.append([_input, _label])
                    line = f.readline()
                    if len(line) > 20000:
                        break
        if self.shuffle:
            random.shuffle(self.data)

    def next(self):
        return super().next()
        batch_data = None
        try:
            data = self.data[self.index : self.index + self.batch_size]
            self.index += self.batch_size
            input = [x[0] for x in data]
            label = [x[1] for x in data]
            if len(input) >= self.batch_size:
                batch_data = {'input': input, 'label': label}
        except:
            pass
        return batch_data
