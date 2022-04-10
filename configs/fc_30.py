# IMDBModel
{
    'max_epoch': 10,
    'model': 'IMDBModel(3000,100,30)',
    'log_interval': 10,
    'train_dataloader': "Dataloader(['dataset/train_10w.data'], batch_size)",
    'valid_dataloader': "Dataloader(['dataset/test_2w.data'], batch_size)",
    'transform': "["
    # "BaseTokenizer(),"
    "BaseTransform('dump/mapping_12w_3000.data',max_word_size=100)," "]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    # 'test':True,
    # 'checkpoint': 'checkpoints/base_best.pkl',
    # 'inference': True,
    'batch_size': 1000,
    'device': 'gpu',
    'name': 'fc_30',
}
