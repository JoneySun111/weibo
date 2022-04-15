{
    'runner': 'CNNRunner',
    'model': 'CNNModel(30,"checkpoints/skipgram_12w_best.pkl")',
    'transform': "[" "BaseTransform('dump/mapping_12w_3000.data',max_word_size=100)]",
    # 'save_after_epoch': True,
    'checkpoint': 'checkpoints/cnn_inference_best.pkl',
    'inference': True,
    'name': 'cnn_inference',
    'batch_size': 1000,
    'device': 'cpu',
}
