{
    'runner': 'CNNRunner',
    'max_epoch': 10,
    'model': 'CNNModel(10,"checkpoints/skipgram_12w_word_best.pkl")',
    'log_interval': 10,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/train_10w_word.data'])"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "OldDataset(['dataset/test_2w_word.data'],)"
    ", batch_size=batch_size, shuffle=True)",
    'transform': "[" 
        "WordTransfomer(),"
        "BaseTransform('dump/tokenizer_mapping_12w_3000.data',max_word_size=100)"
    "]",
    'optimizer': 'optim.Adam',
    'criterion': 'F.nll_loss',
    # 'save_after_epoch': True,
    'name': 'cnn_10_12w_word',
    'batch_size': 1000,
    'device': 'gpu',
}
