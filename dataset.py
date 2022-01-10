import gluonbook as gb
from mxnet.gluon import data as gdata

mnist_train = gdata.vision.FashionMNIST(train=True)
mnist_test = gdata.vision.FashionMNIST(train=False)
