{
    'runner': 'NgramRunner',
    'max_epoch': 10,
    'model': 'NgramModel(3000,3,40)',
    'log_interval': 100,
    'train_dataloader': "NgramDataloader(['dataset/train.txt'], batch_size, 3, tokenize=False)",
    'valid_dataloader': "NgramDataloader(['dataset/test.txt'], batch_size, 3, tokenize=False)",
    'transform': "["
    # "BaseTokenizer(),"
    "BaseTransform('dump/tokenizer_mapping_3000.data',max_word_size=0)," "]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    # 'test':True,
    # 'checkpoint': 'checkpoints/best.pkl',
    # 'inference': True,
    'batch_size': 2000,
    'device':'gpu',
}
