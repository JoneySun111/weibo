{
    'runner': 'NovelRunner',
    'max_epoch': 10,
    'model': 'LstmModel(4061,512)',
    'log_interval': 100,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/novel/train.txt'], 50, 10)"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/novel/valid.txt'], 50, 50)"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_novel.data') ]",
    'optimizer': 'optim.Adam',
    # 'criterion': 'F.nll_loss',
    'criterion': 'nn.CrossEntropyLoss()',
    'save_after_epoch': True,
    'name': 'novel1',
    'batch_size': 1024,
    'device': 'gpu',
}
