__author__ = 'syj'
#coding:utf-8
#open the base data,which is exactly right.
#return a dictionary,where subject is the key and stock is the values
class read_baselabel():
    def __init__(self,path):
        self.path_in = path
    def transpose(self):
        result_trans = {}
        stock_names = []
        lines = [line.strip().split('\t') for line in open(self.path_in,'r').readlines()]
        for line in lines:
            if len(line) == 3:
                stock_names.append(line[0])
                for item in line[2].split(';'):
                    if item.strip() in result_trans.keys():
                        result_trans[item.strip()].append(line[0].strip())
                    else:
                        result_trans[item.strip()]=[line[0].strip()]
            else:
                pass
        return result_trans,list(set(stock_names))
