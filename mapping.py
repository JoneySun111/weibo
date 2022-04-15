# 汉字映射到int
import torch
import pickle


class mapping:
    UNK_TAG = "UNK"
    PAD_TAG = "PAD"
    UNK = 1
    PAD = 0

    def __init__(self, max_word_size=-1):
        self.mp = dict()  # counting
        self.max_word_size = max_word_size

    def set_word_size(self, max_word_size):
        self.max_word_size = max_word_size

    def add_word(self, word):
        self.mp.setdefault(word, 0)
        self.mp[word] += 1

    def add_sentence(self, sentence):
        for word in sentence:
            self.add_word(word)

    def add_sentences(self, sentences):
        for sentence in sentences:
            self.add_sentence(sentence)

    def init(self, mapping_size=9999999999, debug=0):
        self.mapping_size = mapping_size
        self.items = list(self.mp.items())
        self.items.sort(key=lambda x: x[1], reverse=True)
        self.word2id = {mapping.UNK_TAG: mapping.UNK, mapping.PAD_TAG: mapping.PAD}
        for i, x in enumerate(self.items):
            self.word2id[x[0]] = i + 2
            if len(self.word2id) >= mapping_size:
                break
        self.id2word = {v: k for k, v in self.word2id.items()}
        del self.items
        self.freqs = {}
        sum = 0
        for key, value in self.mp.items():
            x = self.word_to_id(key).item()
            self.freqs.setdefault(x, 0)
            self.freqs[x] += value
            sum += value
        del self.mp
        self.freqs = {k: v / sum for k, v in self.freqs.items()}
        if debug:
            _lst = sorted(list(self.freqs.items()), key=lambda x: x[1])
            print(_lst[:20])
            print(_lst[-20:])
            print('UNK:', self.freqs[1])

    def word_to_id(self, word):
        return torch.tensor(self.word2id.get(word, mapping.UNK))

    def mapping_from_sentence(self, sentence):
        lst = []
        for i, word in enumerate(sentence):
            if i >= self.max_word_size and self.max_word_size > 0:
                break
            lst.append(self.word_to_id(word))
        if self.max_word_size <= 0:
            return torch.stack(lst)
        return torch.stack(lst + [torch.tensor(mapping.PAD)] * (self.max_word_size - len(lst)))

    def mapping_from_sentences(self, sentences):
        lst = []
        for sentence in sentences:
            lst.append(self.mapping_from_sentence(sentence))
        if len(lst)==0:
            return torch.tensor(lst)
        return torch.stack(lst)

    def id_to_word(self, id):
        if isinstance(id, torch.Tensor):
            id = id.item()
        return self.id2word.get(id, mapping.UNK_TAG)

    def get_sentence(self, ids):
        lst = []
        for id in ids:
            if id != mapping.PAD:
                lst.append(self.id_to_word(id))
        return lst

    def get_sentences(self, ids):
        lst = []
        for id in ids:
            lst.append(self.get_sentence(id))
        return lst

    # def get_frequency(self):
    #     return self.items[: self.mapping_size]

    def pre_work(self, T=0.75):
        self.freqs = {k: v ** T for k, v in self.freqs.items()}
        tot = sum(self.freqs.values())
        self.freqs = {k: v / tot for k, v in self.freqs.items()}
        self.word_freqs = [0] * (max(self.freqs.keys()) + 1)
        for k, v in self.freqs.items():
            self.word_freqs[k] = v
        self.word_freqs = torch.tensor(self.word_freqs)

    def dump(self, path):
        # del self.mp
        # del self.items
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            return obj
