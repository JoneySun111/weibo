import torch
import torch.nn as nn
import torch.nn.functional as F
from mapping import *


class SkipGramModel(nn.Module):
    def __init__(self, vocab_size, embedding_size=50):
        super(SkipGramModel, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.input_emb = nn.Embedding(vocab_size, embedding_size, padding_idx=mapping.PAD)
        self.output_emb = nn.Embedding(vocab_size, embedding_size, padding_idx=mapping.PAD)
        self.input_emb.weight.data.uniform_(-1, 1)
        self.output_emb.weight.data.uniform_(-1, 1)
        # initrange = 0.5 / self.embedding_size
        # self.input_emb.weight.data.uniform_(-initrange, initrange)
        # self.output_emb.weight.data.uniform_(-initrange, initrange)

    def forward(self, input, pos_labels, neg_labels):
        # input_labels:[batch_size]
        # pos_labels:[batch_size, windows_size*2]
        # neg_labels:[batch_size, windows_size * N_SAMPLES]
        input = self.input_emb(input)
        pos = self.output_emb(pos_labels)
        neg = self.output_emb(neg_labels)

        input = input.unsqueeze(2)
        pos_dot = torch.bmm(pos, input).squeeze(2)
        neg_dot = torch.bmm(neg, input).squeeze(2)

        log_pos = F.logsigmoid(pos_dot).sum(1)
        log_neg = F.logsigmoid(neg_dot).sum(1)

        loss = -(log_pos + log_neg)
        return loss.sum(0)
