from util.utils import *


class log:
    def __init__(self, interval=100):
        self.interval = interval
        self.timestamp = get_time_str()
        self.train_log = {}
        self.val_log = {}

    def add_train_log(self, k, v):
        self.train_log[k] = v

    def add_train_logs(self, dct):
        self.train_log += dct

    def add_val_log(self, k, v):
        self.val_log[k] = v

    def log_train(self):
        if self.train_log.get('iter', 0) % self.interval != 0:
            return
        key = list(self.train_log.keys())
        key.remove('epoch')
        key.remove('iter')
        lst = []
        for x in key:
            lst.append('{}: {}'.format(x, self.train_log[x]))
        print(
            '{} - Epoch(train) [{}][{}] {}'.format(
                get_time_str(),
                self.train_log.get('epoch'),
                self.train_log.get('iter'),
                ','.join(lst),
            )
        )

    def log_valid(self):
        key = list(self.val_log.keys())
        key.remove('epoch')
        lst = []
        for x in key:
            lst.append('{}: {}'.format(x, self.val_log[x]))
        print(
            '{} - Epoch(valid) [{}] {}'.format(
                get_time_str(),
                self.val_log.get('epoch'),
                ','.join(lst),
            )
        )
