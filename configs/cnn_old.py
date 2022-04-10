{
    'runner': 'CNNRunner',
    'max_epoch': 10,
    'model': 'CNNModel(100,"checkpoints/skipgram_olddataset_epoch_best.pkl")',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/train.txt'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/test.txt'])"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_3000.data',max_word_size=100)]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    'name': 'cnn_old',
    'batch_size': 100,
    'device': 'gpu',
}
