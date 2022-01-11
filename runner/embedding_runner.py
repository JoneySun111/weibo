import sys

sys.path.append("..")
import torch
from transform.ngram_transfomer import NgramTransfomer

a = NgramTransfomer(2)
t = torch.arange(10)
print(t)
print(a(t))
