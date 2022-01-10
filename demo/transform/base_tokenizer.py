try:
    from minlptokenizer.tokenizer import MiNLPTokenizer
except:
    ...


class BaseTokenizer:
    def __init__(self, granularity='fine'):
        self.tokenizer = MiNLPTokenizer(granularity=granularity)

    def __call__(self, data):
        data = self.tokenizer.cut(data)
        return data
