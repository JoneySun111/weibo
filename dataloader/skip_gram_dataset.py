import torch
import random

class SkipGramDataset(torch.utils.data.Dataset):
    def __init__(self, path_list):
        super().__init__()
        self.path_list=path_list
        assert isinstance(path_list,list)
        self.data=[]
        for file in path_list:
            with open(file,'r')as f:
                now=f.readlines()
                now=list(map(lambda x:x.strip(),now))
                # now=list(filter(lambda x:len(x.strip())>0,now))
                self.data+=now

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# dataset=SkipGramDataset(['dataset/comments.log'])
# print(dataset[1])
# print(len(dataset[1]))
# random.shuffle(dataset.data)
# with open('dataset/comments_test.log','w+') as f:
#     f.write('\n'.join(dataset.data[:50000]))
# with open('dataset/comments_train.log','w+') as f:
#     f.write('\n'.join(dataset.data[50000:50000+60000*10]))
