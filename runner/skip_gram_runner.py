import sys

import torch
from runner import *
from dataloader import *


class SkipGramRunner(BaseRunner):
    def __init__(self, cfg):
        super().__init__(cfg)

    def init_dataloader(self):
        batch_size = self.batch_size
        self.train_dataloader = eval(self.cfg.get("train_dataloader", ""))
        self.valid_dataloader = eval(self.cfg.get("valid_dataloader", ""))

    def run(self):
        self.model.train()
        self.before_run()
        self.before_train_epoch()
        while self.epoch <= self.max_epoch:
            for batch_data in self.train_dataloader:
                assert batch_data is not None, "batch_data error"
                self.before_train_iter()
                self.model.train()
                center_word, pos_words, neg_words = batch_data
                center_word = center_word.to(self.device)  # .unsqueeze(-1)
                pos_words = pos_words.to(self.device).squeeze(-1)
                neg_words = neg_words.to(self.device).squeeze(-1)
                batch_data = {
                    'center_word': center_word,
                    'pos_words': pos_words,
                    'neg_words': neg_words,
                }
                self.loss = self.model(center_word, pos_words, neg_words)
                self.after_train_iter()
                if self.iter == 10000:
                    self.save_checkpoint(
                        self.save_checkpoint(
                            "checkpoints/{}_epoch_{}.pkl".format(self.name, self.epoch)
                        )
                    )

            self.after_train_epoch()
            self.valid()
            self.inner_iter = 0
            self.epoch += 1
            self.before_train_epoch()

        self.after_run()

    def after_train_iter(self):
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
            for batch_data in self.valid_dataloader:
                assert batch_data is not None, "batch_data error"
                self.before_val_iter()
                center_word, pos_words, neg_words = batch_data
                center_word = center_word.to(self.device)  # .unsqueeze(-1)
                pos_words = pos_words.to(self.device).squeeze(-1)
                neg_words = neg_words.to(self.device).squeeze(-1)
                batch_data = {
                    'center_word': center_word,
                    'pos_words': pos_words,
                    'neg_words': neg_words,
                }
                loss = self.model(center_word, pos_words, neg_words)
                self.val_loss += loss
                self.after_val_iter()
        self.val_loss /= self.total

        self.after_val_epoch()
        self.model.train()
