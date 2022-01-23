import sys

# sys.path.append("..")
import torch
from runner import *
from transform.ngram_transfomer import *
from dataloader.ngram_dataloader import *


class NgramRunner(BaseRunner):
    def __init__(self, cfg):
        super().__init__(cfg)

    def run(self):
        self.model.train()
        self.before_run()
        self.before_train_epoch()
        while self.iter <= self.max_iters:
            batch_data = self.train_dataloader.next()
            if batch_data is None:
                self.after_train_epoch()
                self.valid()
                if self.epoch == self.max_epoch:
                    break
                self.train_dataloader.reset()
                batch_data = self.train_dataloader.next()
                self.inner_iter = 0
                self.epoch += 1
                self.before_train_epoch()
            assert batch_data is not None, "batch_data error"
            self.before_train_iter()
            self.model.train()
            for transform in self.transform:
                batch_data['input'] = transform(batch_data['input'])
                batch_data['label'] = transform(batch_data['label'], 'sentence')
            batch_data['label'] = batch_data['label'].squeeze(-1)
            self.target = batch_data['label'].to(self.device)
            t1 = time()
            self.output = self.model(batch_data.get('input').to(self.device))
            self.after_train_iter()
            # if self.iter%1000==0:
            #     for i in range(10):
            #         print(super().test_embedding())
            #     print(super().test_embedding('开心'))
            #     print(super().test_embedding('我'))
            #     print(super().test_embedding('高兴'))

        self.after_run()

    def valid(self):
        self.before_val_epoch()
        self.valid_dataloader.reset()
        self.val_iter = 0
        self.model.eval()
        batch_data = self.valid_dataloader.next()
        with torch.no_grad():
            while batch_data:
                self.before_val_iter()
                for transform in self.transform:
                    batch_data['input'] = transform(batch_data['input'])
                    batch_data['label'] = transform(batch_data['label'], 'sentence')
                batch_data['label'] = batch_data['label'].squeeze(-1)
                target = batch_data['label'].to(self.device)
                output = self.model(batch_data.get('input').to(self.device))
                self.val_loss += self.criterion(output, target, reduction="sum")
                pred = torch.max(output, dim=-1, keepdim=False)[-1]
                # guess
                # mp=self.transform[-1].mp
                # print(mp.get_sentence(target),mp.get_sentence(pred))
                #
                self.correct += pred.eq(target.data).sum()
                self.total += target.shape[0]
                self.after_val_iter()
                batch_data = self.valid_dataloader.next()
        self.val_loss /= self.total

        self.after_val_epoch()
        self.model.train()
