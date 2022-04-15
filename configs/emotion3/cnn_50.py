{
    'runner': 'CNNRunner',
    'max_epoch': 50,
    'model': 'CNNModel(50,"checkpoints/skipgram_dataset3_best.pkl",emotion=3)',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/dataset3_train.data','dataset/mydataset_label.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/mydataset_label.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_dataset3_3000.data',max_word_size=100)]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    'save_after_epoch': True,
    'name': 'cnn_dataset3_50',
    'checkpoint': 'checkpoints/cnn_dataset3_50_best.pkl',
    'batch_size': 1000,
    'device': 'gpu',
}
