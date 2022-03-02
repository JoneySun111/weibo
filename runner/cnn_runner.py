import sys

import torch
from runner import *
from dataloader import *


class CNNRunner(BaseRunner):
    def __init__(self, cfg):
        super().__init__(cfg)

    def init_dataloader(self):
        batch_size = self.batch_size
        self.train_dataloader = eval(self.cfg.get("train_dataloader", ""))
        self.valid_dataloader = eval(self.cfg.get("valid_dataloader", ""))

    def run(self):
        self.model.train()
        self.before_run()
        while self.epoch <= self.max_epoch:
            self.before_train_epoch()
            for input, label in self.train_dataloader:
                assert input is not None, "batch_data error"
                self.before_train_iter()
                self.model.train()
                # center_word = center_word.to(self.device)  # .unsqueeze(-1)
                # pos_words = pos_words.to(self.device).squeeze(-1)
                # neg_words = neg_words.to(self.device).squeeze(-1)
                for transform in self.transform:
                    input = transform(input)
                batch_data = {
                    'input': input.to(self.device),
                    'label': label.to(self.device),
                }
                self.target = batch_data['label']
                self.output = self.model(batch_data['input'])
                self.after_train_iter()

            self.after_train_epoch()
            self.valid()
            self.inner_iter = 0
            self.epoch += 1

        self.after_run()

    def after_train_iter(self):
        return super().after_train_iter()
        # step
        self.inner_iter += 1
        self.iter += 1
        # backward
        self.loss.backward()
        self.optimizer.step()
        # log
        self.log.add_train_log("epoch", self.epoch)
        self.log.add_train_log("iter", self.iter)
        self.log.add_train_log("loss", self.loss)
        self.log.log_train()

    def valid(self):
        self.before_val_epoch()
        self.val_iter = 0
        self.model.eval()
        with torch.no_grad():
            for input, label in self.valid_dataloader:
                self.before_val_iter()
                for transform in self.transform:
                    input = transform(input)
                input = input.to(self.device)
                target = label.to(self.device)
                output = self.model(input)
                self.val_loss += self.criterion(output, target, reduction="sum")
                pred = torch.max(output, dim=-1, keepdim=False)[-1]
                self.correct += pred.eq(target.data).sum()
                self.total += target.shape[0]
                self.after_val_iter()
        self.val_loss /= self.total

        self.after_val_epoch()
        self.model.train()

