# IMDBModel
{
    'max_epoch': 5,
    'model': 'IMDBModel(3000,50,50)',
    'log_interval': 10,
    'train_dataloader': "Dataloader(['dataset/train.txt'], batch_size)",
    'valid_dataloader': "Dataloader(['dataset/test.txt'], batch_size)",
    'transform': "["
    # "BaseTokenizer(),"
    "BaseTransform('dump/mapping_3000.data',max_word_size=50)," "]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    # 'test':True,
    'checkpoint': 'checkpoints/base_best.pkl',
    'inference': True,
    'batch_size': 100,
    'device': 'cpu',
    'name': 'base',
}
