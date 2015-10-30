__author__ = 'syj'
#coding = utf-8
#preprogressing the raw data
#return dic,key:subject and value:stock

class read_rawdata():
    def __init__(self,path):
        self.path = path
    def read_rawdata(self):
        lines = [line_data.split('\t') for line_data in open(self.path,'r').readlines()]
        data_reault = {}
        for line in lines:
            labels = [item.split(':')[0] for item in line[1].split('\001')]
            data_reault[line[0]] = labels
        return data_reault



