from model import *
from util.utils import *
from util.log import *
from dataloader import *
from transform import *
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import math, random


class BaseRunner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.timestamp = get_time_str()
        self.max_epoch = int(cfg.get("max_epoch", 10))
        self.max_iters = int(cfg.get("max_iters", 100000))
        self.log_interval = int(cfg.get("log_interval", 100))
        self.name = cfg.get('name', 'model')
        self.device = cfg.get("device", "cpu")
        if self.device == "gpu":
            self.device = "cuda:0"
        self.model = eval(cfg.get("model")).to(self.device)
        if self.cfg.get("checkpoint", None):
            self.load_checkpoint(cfg.get("checkpoint"))
        self.save_after_epoch = cfg.get("save_after_epoch", False)
        self.batch_size = int(cfg.get("batch_size", 10))
        self.transform = eval(self.cfg.get("transform", "0"))
        if self.cfg.get("test", None):
            self.test_embedding("None")
            return
        if self.cfg.get("inference", None):
            assert "checkpoint" in self.cfg, "inference mode must has checkpoint"
            return

        self.criterion = eval(cfg.get("criterion", '0'))
        self.init_dataloader()
        self.log = log(self.log_interval)
        self.optimizer = eval(cfg.get("optimizer"))(self.model.parameters())
        self.epoch = 1
        self.iter = 1
        self.inner_iter = 0

    def init_dataloader(self):
        batch_size = self.batch_size
        self.train_dataloader = eval(self.cfg.get("train_dataloader", ""))
        self.valid_dataloader = eval(self.cfg.get("valid_dataloader", ""))
        self.train_dataloader.reset()
        self.valid_dataloader.reset()

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
                batch_data["input"] = transform(batch_data["input"])
            self.target = torch.tensor(batch_data["label"]).to(self.device)
            self.output = self.model(batch_data.get("input"))
            self.after_train_iter()

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
                    batch_data["input"] = transform(batch_data["input"])
                target = torch.tensor(batch_data["label"]).to(self.device)
                output = self.model(batch_data.get("input")).to(self.device)
                self.val_loss += self.criterion(output, target, reduction="sum")
                pred = torch.max(output, dim=-1, keepdim=False)[-1]
                self.correct += pred.eq(target.data).sum()
                self.total += target.shape[0]
                self.after_val_iter()
                batch_data = self.valid_dataloader.next()
        self.val_loss /= self.total

        self.after_val_epoch()
        self.model.train()

    def inference(self, batch_data):
        if isinstance(batch_data, str):
            batch_data = [batch_data]
        self.model.eval()
        with torch.no_grad():
            for transform in self.transform:
                batch_data = transform(batch_data)
            output = math.e ** self.model(batch_data)
            pred = torch.max(output, dim=-1, keepdim=False)[-1]
            res = list(zip(batch_data, pred))
            print("\n".join([str(x) for x in res]))
            return output
        ...

    def before_run(self):
        print("model_layers:", self.model)
        self.best = 0

        ...

    def after_run(self):
        ...

    def before_train(self):
        ...

    def before_train_epoch(self):
        ...

    def after_train_epoch(self):
        if self.save_after_epoch:
            self.save_checkpoint("checkpoints/{}_epoch_{}.pkl".format(self.name, self.epoch))
        ...

    def before_train_iter(self):
        # zero_grad
        self.optimizer.zero_grad()

    def after_train_iter(self):
        # step
        self.inner_iter += 1
        self.iter += 1
        # backward
        loss = self.criterion(self.output, self.target)
        loss.backward()
        self.optimizer.step()
        # log
        self.log.add_train_log("epoch", self.epoch)
        self.log.add_train_log("iter", self.iter)
        self.log.add_train_log("loss", loss)
        self.log.log_train()

    def before_val_epoch(self):
        # init val_log
        self.correct = self.total = self.val_loss = 0

    def after_val_epoch(self):
        self.log.add_val_log("epoch", self.epoch)
        self.log.add_val_log("correct", self.correct)
        self.log.add_val_log("total", self.total)
        self.log.add_val_log("loss", self.val_loss)
        acc = torch.true_divide(self.correct, self.total)
        if acc > self.best:
            self.best = acc
            self.save_checkpoint("checkpoints/{}_best.pkl".format(self.name))
        self.log.add_val_log("acc", acc)
        self.log.log_valid()

    def before_val_iter(self):
        ...

    def after_val_iter(self):
        ...

    def save_checkpoint(self, path):
        mkdir(path)
        torch.save(self.model, path)

    def load_checkpoint(self, path):
        self.model = torch.load(path)
        print("load_checkpoint from {}".format(path))

    def test_embedding(self, key="None"):
        def dis(a, b):
            sum = (a - b) ** 2
            sum = sum.sum(0) ** 0.5
            return sum

        mp = self.transform[-1].mp
        embedding = self.model.embedding
        if key == "None" or mp.word_to_id(key) == mapping.UNK:
            key = mp.id_to_word(random.randint(0, len(mp.word2id)))
        res = {"key": key}
        key = self.transform[-1]([[key]])
        key = embedding(key)[0][0]
        arr = []
        for k, v in mp.word2id.items():
            now = self.transform[-1]([[k]])
            now = embedding(now)[0][0]
            arr.append((k, dis(now, key)))
        arr = sorted(arr, key=lambda x: x[1])
        res["latest"] = arr[:10]
        return res
