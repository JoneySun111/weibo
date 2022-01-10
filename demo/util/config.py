class Config:
    @staticmethod
    def fromfile(filename):
        with open(filename, 'r') as f:
            return eval(f.read())

    @staticmethod
    def from_list(lst):
        dct = {}
        assert len(lst) % 2 == 0, 'config args must be even'
        for i in range(0, len(lst), 2):
            if '--' in lst[i][:2]:
                lst[i] = lst[i][2:]
            dct[lst[i]] = lst[i + 1]
        return dct
