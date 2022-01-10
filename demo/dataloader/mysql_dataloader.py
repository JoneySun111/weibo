import random
from mysql import mysql


class mysql_dataloader:
    def __init__(
        self,
        batch_size=1,
        shuffle=False,
    ):
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.epoch_count = 0

    def reset(
        self,
    ):
        self.epoch_count += 1
        random.seed(123356 + self.epoch_count)
        self.index = 0
        self.page = 0

    def next(self):
        data = None
        try:
            input = [
                x[0]
                for x in mysql.query_comments(
                    where='text!=""', page=self.page, page_size=self.batch_size
                )
            ]
            self.page += 1
            label = [0 for x in input]
            assert len(input) == self.batch_size
            if len(input) >= self.batch_size:
                data = {'input': input, 'label': label}
        except:
            data = None
        return data
