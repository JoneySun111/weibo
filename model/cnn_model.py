from model import *
import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNModel(nn.Module):
    def __init__(self, out_channels, chkpt_path=''):
        super(CNNModel, self).__init__()
        self.max_word_size = 20
        try:
            self.embedding = torch.load(chkpt_path).input_emb
            self.embedding_size = self.embedding.weight.data.shape[-1]
            print(f'load embedding from {chkpt_path} success, embedding_size={self.embedding_size}')
        except:
            ...
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=out_channels,
            kernel_size=(3, self.embedding_size),
            padding=[1, 0],
        )
        self.conv2 = nn.Conv2d(
            in_channels=1,
            out_channels=out_channels,
            kernel_size=(5, self.embedding_size),
            padding=[2, 0],
        )
        self.conv3 = nn.Conv2d(
            in_channels=1,
            out_channels=out_channels,
            kernel_size=(7, self.embedding_size),
            padding=[3, 0],
        )
        self.fc = nn.Linear(out_channels * 3, 2)

    def forward(self, x):
        # x(Batch,length)
        max_word_size = x.shape[1]
        x = self.embedding(x)
        # x(Batch,length,embedding)
        x = x.unsqueeze(dim=1)
        # x(Batch,1,length,embedding)
        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x = torch.cat((x1, x2, x3), 1).squeeze(dim=-1)
        x = F.relu(x)
        x = F.max_pool2d(x, kernel_size=(1, max_word_size)).squeeze(dim=-1)
        x = self.fc(x)
        x = F.dropout(x, p=0.5, training=self.training)
        return F.log_softmax(x, dim=-1)


if __name__ == '__main__':
    x = CNNModel(100)
    a = torch.rand((10, 20, 30))
    out = x(a)
    print(out)
    print(out.shape)
