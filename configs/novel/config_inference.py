{
    'runner': 'NovelRunner',
    'max_epoch': 10,
    'model': 'LstmModel(4061,256)',
    'log_interval': 100,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/novel/train.txt'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "NovelDataset(['dataset/novel/valid.txt'])"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_novel.data') ]",
    'optimizer': 'optim.Adam',
    # 'criterion': 'F.nll_loss',
    'criterion': 'nn.CrossEntropyLoss()',
    'save_after_epoch': False,
    'name': 'novel',
    'batch_size': 1024,
    'device': 'cpu',
    'checkpoint': 'checkpoints/novel_best.pkl',
    'inference': '包敏哈哈大笑，说道',
    'punc_prob': 1,
}
