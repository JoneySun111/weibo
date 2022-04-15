{
    'runner': 'CNNRunner',
    'model': 'CNNModel(50,"checkpoints/skipgram_dataset3_best.pkl",emotion=3)',
    'transform': "[" "BaseTransform('dump/mapping_dataset3_3000.data',max_word_size=100)]",
    'criterion': 'F.nll_loss',
    'checkpoint': 'checkpoints/cnn_mydataset_best.pkl',
    'inference': True,
    'name': 'cnn_inference',
    'batch_size': 1000,
    'device': 'cpu',
}
