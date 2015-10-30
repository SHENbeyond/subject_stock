__author__ = 'syj'
#coding:utf-8
class read_word2vec():
    def __init__(self,path):
        self.path  = path
    def read_w2v(self):
        ff = open(self.path,'r').readlines()
        jieguo = {}
        for line in ff:
            lines = line.strip().split(' ')
            jieguo[lines[0].strip()] = lines[1:]
        return jieguo