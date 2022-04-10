{
    'runner': 'SkipGramRunner',
    'max_epoch': 10,
    'model': 'SkipGramModel(3000,40)',
    'log_interval': 100,
    'train_dataloader': "torch.utils.data.DataLoader(dataset="
    "SkipGramDataset(['dataset/train_10w.data'], mapping_path='dump/mapping_12w_3000.data')"
    ", batch_size=batch_size, shuffle=True)",
    'valid_dataloader': "torch.utils.data.DataLoader(dataset="
    "SkipGramDataset(['dataset/test_2w.data'], mapping_path='dump/mapping_12w_3000.data')"
    ", batch_size=batch_size, shuffle=True)",
    # 'transform': "["
    #     # "BaseTokenizer(),"
    #     "BaseTransform('dump/tokenizer_mapping_3000.data',max_word_size=0)," "]",
    'optimizer': 'optim.Adam',
    'save_after_epoch': True,
    'name': 'skipgram_12w',
    'batch_size': 1000,
    'device': 'gpu',
}
