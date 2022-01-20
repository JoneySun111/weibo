import torch
import torch.nn as nn
import torch.nn.functional as F
from mapping import *


class SkipGramModel(nn.Module):
    def __init__(self, vocab_size, embedding_size=50):
        super(SkipGramModel, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.input_emb = nn.Embedding(vocab_size, embedding_size)
        self.output_emb = nn.Embedding(vocab_size, embedding_size)
        self.input_emb.weight.data.uniform_(-1, 1)
        self.output_emb.weight.data.uniform_(-1, 1)
