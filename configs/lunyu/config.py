{
    'runner': 'NovelRunner',
    'max_epoch': 20,
    'model': 'LstmModel(1359,256)',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/lunyu/train.txt'], 80, 10)"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/lunyu/valid.txt'], 50, 10)"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/lunyu.data') ]",
    'optimizer': 'optim.Adam',
    # 'criterion': 'F.nll_loss',
    'criterion': 'nn.CrossEntropyLoss()',
    'save_after_epoch': True,
    'name': 'lunyu',
    'batch_size': 1024,
    'device': 'gpu',
}
