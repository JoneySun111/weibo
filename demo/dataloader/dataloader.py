import random


class dataloader:
    def __init__(
        self,
        path_list,
        batch_size=1,
        shuffle=True,
    ):
        assert isinstance(path_list, list)
        self.path_list = path_list
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.epoch_count = 0

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
                    label = int(line[1])
                    input = ','.join(line[2:])
                    self.data.append([input, label])
                    line = f.readline()
        if self.shuffle:
            random.shuffle(self.data)

    def next(self):
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
