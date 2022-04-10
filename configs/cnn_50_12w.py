{
    'runner': 'CNNRunner',
    'max_epoch': 5,
    'model': 'CNNModel(50,"checkpoints/skipgram_12w_best.pkl")',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/train_10w.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/test_2w.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" "BaseTransform('dump/mapping_12w_3000.data',max_word_size=100)]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    'name': 'cnn_50_12w',
    'batch_size': 1000,
    'device': 'gpu',
}
