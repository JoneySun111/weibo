try:
    from minlptokenizer.tokenizer import MiNLPTokenizer
except:
    ...


class BaseTokenizer:
    def __init__(self, granularity='fine'):
        self.tokenizer = MiNLPTokenizer(granularity=granularity)

    def __call__(self, data):
        if isinstance(data, list):
            data = list(map(lambda x: x if x != '' else ' '), data)
        data = self.tokenizer.cut(data)
        return data
