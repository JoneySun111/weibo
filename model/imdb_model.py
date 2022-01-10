import torch
import torch.nn as nn
import torch.nn.functional as F
from mapping import *


class IMDBModel(nn.Module):
    def __init__(self, vocab_size, max_len, embedding_size=50):
        super(IMDBModel, self).__init__()
        self.embedding = nn.Embedding(
            vocab_size, embedding_size, padding_idx=mapping.PAD
        )  # [Nvocab_size,embedding_size]
        self.fc = nn.Linear(max_len * embedding_size, 2)  # [max_len*embedding_size,2]

    def forward(self, x):
        # x.shape([batch_size,max_len,vocab_size])
        embed = self.embedding(x)  # [batch_size,max_len,embedding_size]
        # print("embed.shape",embed.shape)
        embed = embed.view(x.size(0), -1)
        out = self.fc(embed)
        return F.log_softmax(out, dim=-1)
