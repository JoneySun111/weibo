from time import time, sleep
import torch
from mapping import *
from dataloader import *
from model.imdb_model import IMDBModel

try:
    from minlptokenizer.tokenizer import MiNLPTokenizer
except:
    ...


def test_dataloader():
    test_dataloader = Dataloader(['dataset/test.txt'], 10, False)
    test_dataloader.reset()
    for i in range(100000):
        print(test_dataloader.next())


batch_size = 100
mapping_size = 3000
max_word_size = 100


def test_mapping():
    dataset = OldDataset(['dataset/train.txt', 'dataset/test.txt'])
    dataloader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)
    print(len(dataset))
    # mp=mapping.load('dump/tokenizer_mapping_comments_3000.data')
    # print(len(mp.mp))
    # print(list(mp.mp.items())[:30])

    mp = mapping()
    # mp = mapping.load('dump/mapping_3000.data')
    # print(data['input'])
    # print(mp.mapping_from_sentences(data['input']))
    # print(mp.get_sentences(mp.mapping_from_sentences(data['input'])))

    # tokenizer = MiNLPTokenizer(granularity='fine')
    for i, data in enumerate(dataloader):
        data = data[0]
        mp.add_sentences(data)
        if i % 10 == 1:
            print(f'{i} % {len(dataloader)}')
            # sleep(0.4)
    mp.init(mapping_size, debug=1)
    print(mp.get_sentence(range(0, 20)))
    mp.dump('dump/mapping_3000.data')
    # mp=mapping.load('dump/mapping_comments_3000.data')
    # print(mp.mapping_from_sentences(data['input']).cuda())
    # print(mp.get_idx())
    # print(mp.get_frequency())


def test_tokenizer():
    # train_dataloader = mysql_dataloader(10,shuffle=False)
    # train_dataloader.reset()
    tokenizer = MiNLPTokenizer(granularity='fine')  # fine：细粒度，coarse：粗粒度，默认为细粒度
    train_dataloader = Dataloader(['dataset/train.txt'], batch_size)
    train_dataloader.reset()
    data = train_dataloader.next()
    mp = mapping(max_word_size)
    # mp = mapping.load('dump/tokenizer_mapping_3000.data')
    # print(mp.mapping_from_sentence(tokenizer.cut('我觉得你是傻子')))
    # print(mp.mapping_from_sentence(tokenizer.cut('他跟我也觉得你不是是傻子')))
    # print(mp.get_idx())
    while data:
        mp.add_sentences(tokenizer.cut(data.get('input')))
        data = train_dataloader.next()
    mp.init(mapping_size)
    mp.dump('dump/tokenizer_mapping_3000.data')
    # print(mp.get_idx())
    # print(mp.get_frequency())

    # while data:
    #     print(data['input'])
    #     print(tokenizer.cut(data['input']))
    #     data=train_dataloader.next()
    #     break
    # print(tokenizer.cut('今天天气怎么样？'))


def test_model():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch import optim

    # mp = mapping.load('dump/mapping_3000.data')
    mp = mapping.load('dump/tokenizer_mapping_3000.data')
    mp.set_word_size(max_word_size)
    vocab_size = mp.mapping_size
    device = 'cuda:0'
    device = 'cpu'
    imdb_model = IMDBModel(vocab_size, max_word_size).to(device)
    # print(list(imdb_model.parameters()))
    optimizer = optim.Adam(imdb_model.parameters())
    criterion = nn.CrossEntropyLoss()
    tokenizer = MiNLPTokenizer(granularity='fine')
    # print(imdb_model)

    train_dataloader = Dataloader(['dataset/train.txt'], batch_size)
    test_dataloader = Dataloader(['dataset/test.txt'], batch_size)
    inference_dataloader = mysql_dataloader(batch_size)

    def train(epoch):
        imdb_model.train()
        step = 0
        train_dataloader.reset()
        data = train_dataloader.next()
        while data:
            optimizer.zero_grad()
            input = mp.mapping_from_sentences(tokenizer.cut(data['input'])).to(device)
            output = imdb_model(input).to(device)
            target = torch.tensor(data['label']).to(device)
            # target = F.one_hot(torch.tensor(target), num_classes=2)
            # print(output.shape,target.shape)
            loss = F.nll_loss(output, target)  # traget需要是[0,9]，不能是[1-10]
            loss.backward()
            # print("loss",loss)
            optimizer.step()
            if step % 10 == 0:
                print('Train Epoch: {} [{})]\tLoss: {:.6f}'.format(epoch, step, loss.item()))
            step += 1
            data = train_dataloader.next()

    def test():
        test_loss = 0
        correct = 0
        total = 0
        imdb_model.eval()
        test_dataloader.reset()
        data = test_dataloader.next()
        with torch.no_grad():
            while data:
                input = mp.mapping_from_sentences(tokenizer.cut(data['input'])).to(device)
                target = torch.tensor(data['label']).to(device)
                output = imdb_model(input).to(device)
                test_loss += F.nll_loss(output, target, reduction="sum")
                pred = torch.max(output, dim=-1, keepdim=False)[-1]
                correct += pred.eq(target.data).sum()
                total += target.shape[0]
                # print(correct,total)
                data = test_dataloader.next()
            test_loss = test_loss / total
            print(
                '\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
                    test_loss, correct, total, 100.0 * correct / total
                )
            )

    def inference():
        imdb_model.eval()
        inference_dataloader.reset()
        data = inference_dataloader.next()
        with torch.no_grad():
            while data:
                input = mp.mapping_from_sentences(tokenizer.cut(data['input'])).to(device)
                target = torch.tensor(data['label']).to(device)
                output = imdb_model(input).to(device)
                pred = torch.max(output, dim=-1, keepdim=False)[-1]
                res = list(zip(data['input'], pred))
                print('\n'.join([str(x) for x in res]))
                # print(correct,total)
                data = inference_dataloader.next()
                break

    # inference()
    # return
    test()
    for i in range(5):
        train(i)
        test()
        inference()
    # test()

def read_csv():
    import pandas as pd
    import random
    path='F:\Desktop\毕设\ChineseNlpCorpus-master\weibo_senti_100k\weibo_senti_100k'
    pd_all = pd.read_csv(path + '\weibo_senti_100k.csv')
    # print(pd_all.sample(20))
    data=[]
    for i in range(len(pd_all)):
        data.append({
            'label':pd_all['label'][i],    
            'review':pd_all['review'][i],
        })
    random.shuffle(data)
    with open("dataset/train_10w.data","w",encoding='utf-8') as f:
        for i in range(100000):
            f.write(",{},{}\n".format(data[i]['label'],data[i]['review']))
    with open("dataset/test_2w.data","w",encoding='utf-8') as f:
        for i in range(100000,len(data)):
            f.write(",{},{}\n".format(data[i]['label'],data[i]['review']))

def save_mapping():
    dataset = OldDataset(['dataset/train_10w.data', 'dataset/test_2w.data'])
    dataloader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)
    print(len(dataset))

    mp = mapping()

    # tokenizer = MiNLPTokenizer(granularity='fine')
    for i, data in enumerate(dataloader):
        data = data[0]
        mp.add_sentences(data)
        if i % 100 == 1:
            print(f'{i} % {len(dataloader)}')
            # sleep(0.4)
    mp.init(mapping_size, debug=1)
    print(mp.get_sentence(range(0, 20)))
    mp.dump('dump/mapping_12w_3000.data')


if __name__ == '__main__':
    # print(torch.__version__)
    # print(torch.cuda.is_available())
    # test_mapping()
    # test_tokenizer()
    # test_model()
    # read_csv()
    save_mapping()
