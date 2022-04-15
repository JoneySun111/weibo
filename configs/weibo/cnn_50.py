{
    'runner': 'CNNRunner',
    'max_epoch': 10,
    'model': 'CNNModel(50,"checkpoints/skipgram_mydataset_best.pkl",emotion=3)',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/mydataset_train.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/mydataset_test.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_mydataset_3000.data',max_word_size=100)]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    'save_after_epoch': True,
    'name': 'cnn_mydataset',
    'checkpoint': 'checkpoints/cnn_mydataset_best.pkl',
    'batch_size': 1000,
    'device': 'gpu',
}
