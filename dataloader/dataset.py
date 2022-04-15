import random
import torch

# import sys
# sys.path.append('..')
# from transform.word_transform import *
# from torch.utils.data import Dataset


class TxtDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        path_list,
    ):
        super().__init__()
        self.path_list = path_list
        assert isinstance(path_list, list)
        self.data = []
        for file in path_list:
            with open(file, 'r', encoding='utf8') as f:
                now = f.readlines()
                now = list(map(lambda x: x.strip(), now))
                self.data += now

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


class OldDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        path_list,
    ):
        super().__init__()
        self.path_list = path_list
        assert isinstance(path_list, list)
        self.data = []
        self.label = []
        for file in path_list:
            with open(file, 'r', encoding='utf8') as f:
                now = f.readlines()
                now = list(map(lambda x: x.strip(), now))
                self.label += list(map(lambda x: x.split(',')[1], now))
                self.data += list(map(lambda x: ','.join(x.split(',')[2:]), now))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], int(self.label[idx])


class WordDataset(OldDataset):
    def __init__(self, path_list):
        super().__init__(path_list)
        self.data = list(map(lambda x: eval(x), self.data))
        # self.data = WordTransfomer(max_word_size)(self.data)


if __name__ == '__main__':
    dataset = OldDataset(['dataset/train_10w_word.data'])
    print(len(dataset[0][0]))
    # import torch
    batch_size = 10
    dataloader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)
    for x in dataloader:
        print(x)
        break
    # for x in

# class TxtDataset(Dataset):
#     def __init__(
#         self,
#         path,
#     ):
#         assert isinstance(path, list)
#         self.path_list = path_list

#     def reset(
#         self,
#     ):
#         self.epoch_count += 1
#         random.seed(123356 + self.epoch_count)
#         if self.shuffle:
#             random.shuffle(self.path_list)
#         self.index = 0
#         self.data = []
#         for path in self.path_list:
#             with open(path, 'r', encoding='utf-8') as f:
#                 line = f.readline()
#                 while line:
#                     line = line.replace('\u200b', '').strip().split(',')
#                     label = int(line[1])
#                     input = ','.join(line[2:])
#                     self.data.append([input, label])
#                     line = f.readline()
#         if self.shuffle:
#             random.shuffle(self.data)

#     def next(self):
#         data = None
#         try:
#             data = self.data[self.index : self.index + self.batch_size]
#             self.index += self.batch_size
#             input = [x[0] for x in data]
#             label = [x[1] for x in data]
#             if len(input) >= self.batch_size:
#                 data = {'input': input, 'label': label}
#         except:
#             pass
#         return data
