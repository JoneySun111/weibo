{
    'max_epoch': 5,
    'model': 'IMDBModel(3000,50,50)',
    'log_interval': 10,
    'train_dataloader': "dataloader(['dataset/train.txt'], batch_size)",
    'valid_dataloader': "dataloader(['dataset/test.txt'], batch_size)",
    'transform': "["
    "BaseTokenizer(),"
    "BaseTransform('dump/tokenizer_mapping_3000.data',max_word_size=50),"
    "]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    'save_after_epoch': True,
    # 'test':True,
    'checkpoint': 'checkpoints/best.pkl',
    # 'inference': True,
    'batch_size': 100,
}
