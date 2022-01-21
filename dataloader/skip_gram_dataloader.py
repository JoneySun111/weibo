import torch

from dataloader import *

class SkipGramDataloader(Dataloader):
    def __init__(self,path_list):
        assert isinstance(path_list, list)
        self.path_list=path_list
        