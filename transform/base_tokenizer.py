try:
    from minlptokenizer.tokenizer import MiNLPTokenizer
except:
    ...


class BaseTokenizer:
    def __init__(self, granularity='fine'):
        self.tokenizer = MiNLPTokenizer(granularity=granularity)

    def __call__(self, data):
        if not isinstance(data, list):
            return self.tokenizer.cut(data)
        data1 = list(map(lambda x: x if x.strip() != '' else '#', data))
        data1 = self.tokenizer.cut(data1)
        data = list(map(lambda x: [''] if len(x) == 1 and x[0] == '#' else x, data1))
        return data
