# -*- coding: utf-8 -*-
import torch
import random
import sys
sys.path.append('..')
from mapping import *


class SkipGramDataset(torch.utils.data.Dataset):
    def __init__(self, path_list, mapping_path, window_size=3, n_samples=1):
        super().__init__()
        self.path_list = path_list
        self.window_size = window_size
        self.n_samples = n_samples
        assert isinstance(path_list, list)
        self.mapping=mapping.load(mapping_path)
        self.data = []
        self.idx = []
        for file in path_list:
            with open(file, 'r', encoding='utf8') as f:
                now = f.readlines()
                now = list(map(lambda x: x.strip(), now))
                self.data += now
        for i, line in enumerate(self.data):
            self.idx += [(i, j) for j in range(len(line) - window_size)]

    def __len__(self):
        return len(self.idx)

    def __getitem__(self, idx):
        x, y = self.idx[idx]
        print(x, y)
        center_word = self.data[x][y]
        pos_words = self.data[x][max(0,y-self.window_size):y]+self.data[x][y+1:min(len(self.data[x]),y+1+self.window_size)]
        return center_word,pos_words

if __name__=='__main__':
    dataset = SkipGramDataset(['../dataset/comments.data'],mapping_path='../dump/mapping_comments_3000.data')
    print(len(dataset))
    print(dataset.data[0])
    print(dataset.data[1])
    for i in range(10):
        print(dataset[i])
    # print(dataset[1])
    # print(len(dataset[1]))
    # random.shuffle(dataset.data)
    # with open('dataset/comments_test.log','w+') as f:
    #     f.write('\n'.join(dataset.data[:50000]))
    # with open('dataset/comments_train.log','w+') as f:
    #     f.write('\n'.join(dataset.data[50000:50000+60000*10]))
