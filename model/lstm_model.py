import torch
import torch.nn as nn
import torch.nn.functional as F


class LstmModel(nn.Module):
    def __init__(self, vocab_size, hidden_size):
        super(LstmModel, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.batch_first = False
        self.bidirectional = False
        self.lstm = nn.LSTM(vocab_size, hidden_size)
        self.out = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        x = F.one_hot(x, num_classes=self.vocab_size)
        # x.shape([batch_size, 1, vocab_size])
        batch_size = x.shape[0]
        x = x.transpose(0, 1)
        # x.shape([1, batch_size, vocab_size])
        if not hidden:
            D = 2 if self.bidirectional else 1
            hidden = (
                torch.zeros(D, batch_size, self.hidden_size).to(x.device),
                torch.zeros(D, batch_size, self.hidden_size).to(x.device),
            )
        _, hidden = self.lstm(x.float(), hidden)
        out = self.out(hidden[0]).squeeze(0)
        return out, hidden
