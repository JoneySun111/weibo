import time
import os


def get_time_str():
    '''get_time_str.'''
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())


def mkdir(path):
    os.system('mkdir -p {}'.format(os.path.join(*path.split('/')[:-1])))
