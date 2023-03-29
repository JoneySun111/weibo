import torch
from runner import *
from dataloader.dataset import *
import string
from util.utils import is_punctuation

class NovelRunner(BaseRunner):
    def __init__(self, cfg):
        super().__init__(cfg)
        if cfg.get('inference', None):
            self.inference(cfg.get('inference'))
            return
    
    def init_dataloader(self):
        batch_size = self.batch_size
        self.train_dataloader = eval(self.cfg.get("train_dataloader", ""))
        self.valid_dataloader = eval(self.cfg.get("valid_dataloader", ""))
    
    def run(self):
        self.model.train()
        self.before_run()
        while self.epoch <= self.max_epoch:
            self.before_train_epoch()
            for batch_input in self.train_dataloader:
                assert batch_input is not None, "batch_data error"
                for transform in self.transform:
                    batch_input = transform(batch_input)
                hidden = None
                for j in range(batch_input.shape[1] - 1):
                    batch_data = {
                        'input': batch_input[:,j:j+1].to(self.device),
                        'label': batch_input[:,j + 1].to(self.device),
                    }
                    self.before_train_iter()
                    self.model.train()
                    if hidden:
                        hidden = [x.detach() for x in hidden]
                    self.output, hidden = self.model(batch_data['input'], hidden)
                    # self.pred = torch.max(output, dim=-1, keepdim=False)[-1]
                    self.target = batch_data['label']
                    self.after_train_iter()

            self.after_train_epoch()
            self.valid()
            self.inner_iter = 0
            self.epoch += 1

        self.after_run()

    def valid(self):
        self.before_val_epoch()
        self.val_iter = 0
        self.model.eval()
        with torch.no_grad():
            for batch_input in self.valid_dataloader:
                assert batch_input is not None, "batch_data error"
                for transform in self.transform:
                    batch_input = transform(batch_input)
                hidden = None
                for j in range(batch_input.shape[1] - 1):
                    batch_data = {
                        'input': batch_input[:,j:j+1].to(self.device),
                        'label': batch_input[:,j + 1].to(self.device),
                    }
                    self.before_val_iter()
                    if hidden:
                        hidden = [x.detach() for x in hidden]
                    output, hidden = self.model(batch_data['input'], hidden)
                    pred = torch.max(output, dim=-1, keepdim=False)[-1]
                    target = batch_data['label']
                    self.val_loss += self.criterion(output, target)
                    self.correct += pred.eq(target.data).sum()
                    self.total += target.shape[0]
                    self.after_val_iter()
        self.val_loss /= self.total

        self.after_val_epoch()
        self.model.train()
    
    def test_embedding(self, key="None"):
        return self.inference(key)

    def inference(self, sentence = '', word_count = 100):
        with torch.no_grad():
            mp = self.transform[-1].mp
            # final_prob = torch.ones([1, len(mp.id2word)]).float().to(self.device)
            # for id,word in mp.id2word.items():
            #     if is_punctuation(word):
            #         final_prob[0][id] = self.cfg.get('punc_prob', 1)
            def get_input(sentence):
                batch_input = [list(sentence)]
                for transform in self.transform:
                    batch_input = transform(batch_input)
                return batch_input
            batch_input = get_input(sentence)
            hidden = None
            result = []
            for _ in range(word_count):
                output, hidden = self.model(batch_input.to(self.device), hidden)
                # output = output * final_prob
                prob = torch.nn.Softmax(1)(output)
                # pred = torch.max(output, dim=-1, keepdim=False)[-1]
                # values, index = torch.topk(output, 10)
                # values = values.squeeze(0)
                # index = index.squeeze(0)
                pred = torch.multinomial(prob, 1)
                pred = mp.id_to_word(pred)
                result.append(pred)
                batch_input = get_input(pred)
            print(''.join(result))
            return ''.join(result)
            