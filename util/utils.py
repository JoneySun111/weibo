import time
import os
import torch


def get_time_str():
    '''get_time_str.'''
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())


def mkdir(path):
    path = path.split("/")[:-1]
    cmd = "mkdir "
    if len(path) > 1:
        cmd += "-p "
    else:
        cmd += os.path.join(*path)
    os.system(cmd)
    print("cmd: ", cmd)


def resize0(t, dim=0, target_size=0):
    if t.shape[dim] == target_size:
        return t
    shape = list(t.shape)
    shape[dim] = target_size - shape[dim]
    return torch.concat((t, torch.zeros(shape, dtype=t.dtype, device=t.device)), dim)


if __name__ == '__main__':
    t = torch.ones([2, 2])
    print(t)
    t = resize0(t, 0, 3)
    print(t)
