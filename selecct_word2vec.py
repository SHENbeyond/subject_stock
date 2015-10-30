__author__ = 'syj'
import sys
import os
from read_rawdata import read_rawdata
path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_in = path + "/word2vec.txt"
path_out = path+"/word2vec_item_only.txt"
path_raw_data = path+"/stock_list_result.txt"
raw_data = read_rawdata(path_raw_data)
raw_data_dic = raw_data.read_rawdata()


def set_item(item_dic):
    items_all = []
    for item in item_dic:
        items_all.append(item)
        items_all.extend(item_dic[item])
    #return items_all
    return set(items_all)

items_all = set_item(raw_data_dic)
#print items_all[0]
#print type(items_all[0])
ff_in = open(path_in,'r')
ff_out = open(path_out,'w')
aa = 0
while True:
    line = ff_in.readline()
    if line:
        word = line.strip().split(' ',1)[0]
        print word,type(word)
        if word in items_all:
            ff_out.write(line)
        else:
            pass
    else:
        break
    aa+=1
ff_in.close()
ff_out.close()
