import torch
import torch.nn as nn
import torch.nn.functional as F
from mapping import *


class NgramModel(torch.nn.Module):
    def __init__(self, vocab_size, context_size, embedding_size=50):
        super(NgramModel, self).__init__()
        self.embedding = nn.Embedding(
            vocab_size, embedding_size, padding_idx=mapping.PAD
        )  # [vocab_size,embedding_size]
        self.linear1 = nn.Linear(context_size * embedding_size, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, x):
        # x.shape([batch_size,max_len,vocab_size])
        embed = self.embedding(x)  # [batch_size,max_len,embedding_size]
        # print("embed.shape",embed.shape)
        embed = embed.view(x.size(0), -1)
        out = self.linear1(embed)
        out = F.relu(out)
        out = self.linear2(out)
        return F.log_softmax(out, dim=-1)
