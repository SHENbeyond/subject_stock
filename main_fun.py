#coding:utf-8
import math
import copy
from read_baselabel import read_baselabel
from read_word2vec import read_word2vec
import sys,os
from operator import itemgetter
from pyltp import Segmentor
from collections import Counter


segmentor = Segmentor()
segmentor.load("/data0/shenyanjun/ltp_data/cws.model")
path = os.path.abspath(os.path.dirname(sys.argv[0]))

path_rule_for_stock=path+"/stock_to_theme.txt"
path_base_label = path+"/stock_list_result.txt"
path_word2vec = path+"/word2vec_item_only.txt"
base_label = read_baselabel(path_base_label)
base_label_dic,stock_names = base_label.transpose()

word2vec = read_word2vec(path_word2vec)
word2vec_dic = word2vec.read_w2v()

def makeDict(path1):
    #将规则存入dict,key为股票，value为股票可出现的概念
    dict = {}
    fin = open(path1,'r')
    for line in fin:
        line1 = line.strip().split('\t')
        stock = line1[0]
        concepts = line1[1].strip().split('\001')
        if stock not in dict:
            dict[stock] = []
            for key in concepts:
                dict[stock].append(key)
    fin.close()
    return dict

def counter_stock_in_line(line):
    words = list(segmentor.segment(line))
    word_dic = Counter(words)
    return word_dic

def get_relation_by_query(corpus_path, stock_names):
    corpus = open(corpus_path,'r')
    result = {}
    for kk,line in enumerate(corpus.readlines()):
        print kk
        temp_line = line.strip().split("\001")
        word_dic_line = counter_stock_in_line(line)
        if temp_line[0] in result:
            for stock in stock_names:
                if stock in line:
                    result[temp_line[0]][stock] += word_dic_line[stock]
        else:# temp_line[0] not  in result
            temp_dic = {}
            for stock in stock_names:
                if stock in line:
                    temp_dic[stock] = word_dic_line[stock]
                else:
                    temp_dic[stock] = 0
            result[temp_line[0]] = temp_dic #result[i] 仍为字典
    result_dic = copy.deepcopy(result)
    for topic in result:
        sorted_tuple = sorted(result[topic].iteritems(), key=itemgetter(1), reverse=True)
        #sorted_tuple 为元组的列表
        res_list = []
        for stock,value in sorted_tuple:
            if not dict.has_key(stock):
                res_list.append((stock,value))
                continue
            else:#stock 在 规则dict中
                if topic in dict[stock]:
                    res_list.append((stock,value))
                    continue
                else:#概念不在股票对应的概念中
                    print topic + " " + stock
        result[topic] = res_list
        #结果为按照股票DF值排序
    return result,result_dic

def get_relation_by_ycj(file_ycj):
    stock_names = []
    result = {}
    for line in file_ycj:
        line = line.split("\t")
        if not line[0]:
            continue
        stock_names.append(line[0]) #line[0]为股票名称,stock_names中可能有重复
        if len(line)<3:
            continue
        for topic in line[2].split(";"):
            if topic not in result:
                result[topic] = [line[0]] #result[topic] 为列表，
            else:
                result[topic].append(line[0])
    return result, stock_names
    #result为字典，存储 主题 与 股票的映射
    #strcok_names 存储第一列的股票名称

def theme_stock_tf_couter(result_query,dict,result_ycj):
    result = {}
    for topic in result_query: #topic 即为字典的 key
        result[topic] = []
        if len(topic.strip()) == 0:
            continue
        if not result_query[topic]:
            continue

        temp_list = []  #存储结果的列表
        temp_list1 = [] #存储权重没到5的情况
        max_num = 5
        for stock_value in result_query[topic]:
            if stock_value[0] not in dict.keys():
                max_num = stock_value[1]
                break
            else:
                if topic in dict[stock_value[0]]:
                    max_num = stock_value[1]
                    break
                else:
                    pass
        for key,value in result_query[topic]: #result_query[topic] 为元组的列表
            if value == 0:
                break
            if not key:
                continue
            if len(key.strip()) == 0:
                continue
            if value >= max_num/4:
                result[topic].append(key)
                temp_list.append(key) #此时 len(temp_list) != 0

        if topic in result_ycj:
            if len(topic.strip()) == 0:
                continue
            for item in result_ycj[topic]:
                if item in temp_list:
                    continue
                else:
                    if item not in dict:
                        temp_list.append(item)
                        result[topic].append(item)
                    else: #item 在规则字典中
                        if topic in dict[item]:
                            temp_list.append(item)
                            result[topic].append(item)
                        else:
                            pass

                if item in temp_list1:
                    continue
                else:
                    temp_list1.append(item)
    return result

#cos function:calculate cosine value of two vectors
def sim_cos(vector1,vector2):
    psum = sum([float(vector1[i])*float(vector2[i]) for i in range(len(vector1))])
    sum1sq = sum([pow(float(vec1),2) for vec1 in vector1])
    sum2sq = sum([pow(float(vec2),2) for vec2 in vector2])
    den  = math.sqrt(sum1sq*sum2sq)
    if den == 0:
        return  0
    else:
        return float(psum)/den


def select_standard(list1,list2):
    a = -1
    for loc,word in enumerate(list1):
        if word in list2:
            a = loc
            break
        else:
            pass
    return a

def sim_average(item,list,word2vec_keys,word2vec_dic):
    list_new = [kk for kk in list if kk.strip() in word2vec_keys]
    if list_new:
        sim_sum = sum([sim_cos(word2vec_dic[item],word2vec_dic[stock]) for stock in list_new])
        return sim_sum/float(len(list_new))
    else:
        return ''

def sim_overall(w2v_judge,word2vec_dic):
    result = []
    for loc1,stock1 in enumerate(w2c_judge):
        result.append([])
        if loc1 == 0:
            result[loc1].append(1.0)
        else:
            for loc2,stock2 in enumerate(w2v_judge[:loc1]):
                sim_value = sim_cos(word2vec_dic[stock1],word2vec_dic[stock2])
                result[loc1].append(sim_value)
    return [sum(value)/float(len(value)) for value in result]

if __name__ == "__main__":
    if len(sys.argv)!=4:
        sys.exit(1)
    src = sys.argv[1] #读入语料file
    dest1 = sys.argv[2] #输出结果filename
    dest2 = sys.argv[3] #输出标记为tf的结果
    dir = sys.path[0]
    os.chdir(dir)

    dict = makeDict(path_rule_for_stock)
    result_query,result_dic_tf = get_relation_by_query(src, stock_names)
    raw_data_dic = theme_stock_tf_couter(result_query,dict,base_label_dic)
    ff1_out = open(dest1,'w')
    ff2_out = open(dest2,'w')
    result = {}
    for subject in raw_data_dic.keys():
        result[subject]=[]
        if subject in base_label_dic.keys():
            intersection = list(set(base_label_dic[subject]).intersection(set(raw_data_dic[subject])))
        else:
            intersection = []
        w2c_judge = [kk for kk in raw_data_dic[subject] if kk in word2vec_dic.keys()]
        if len(w2c_judge)>1:
            sim_allvalue = sim_overall(w2c_judge,word2vec_dic)
        else:
            sim_allvalue = []
        print 'ok',sim_allvalue
        for stock in raw_data_dic[subject]:
            if stock in intersection:
                result[subject].append((stock,1))
            elif w2c_judge and intersection and stock in w2c_judge:
                sim_value = sim_average(stock,intersection,word2vec_dic.keys(),word2vec_dic)
                if sim_value >= 0.8:
                    result[subject].append((stock,sim_value))
            elif len(w2c_judge)>1 and not intersection and stock in w2c_judge:
                sim_value_all = sim_allvalue[w2c_judge.index(stock)]
                if sim_value_all >= 0.6:
                    result[subject].append((stock,sim_value_all))
            else:
                result[subject].append((stock,0.0))
    for subject_k in result.keys():
        ff1_out.write(subject_k+'\t')
        ff2_out.write(subject_k+'\t')
        print subject_k
        topic_dic = []
        stocks = sorted(result[subject_k],key=itemgetter(1),reverse=True)
        for stock in stocks[:-1]:
            ff1_out.write(stock[0]+':'+str(stock[1])+'\001')
            if stock[0] in result_dic_tf[subject_k].keys():
                topic_dic.append((stock[0],result_dic_tf[subject_k][stock[0]]))
            else:
                topic_dic.append((stock[0],0))
        if stocks:
            ff1_out.write(stocks[-1][0]+':'+str(stocks[-1][1])+'\n')
            if stocks[-1][0] in result_dic_tf[subject_k].keys():
                topic_dic.append((stocks[-1][0],result_dic_tf[subject_k][stocks[-1][0]]))
            else:
                topic_dic.append((stocks[-1][0],0))
        stocks_dic = sorted(topic_dic,key=itemgetter(1),reverse=True)
        print stocks_dic
        des_w = ''
        for stock_tf in stocks_dic:
            if stock_tf[1] > 0:
                des_w+=stock_tf[0]+':'+str(stock_tf[1])+'\001'
            else:
                print 'okok'
                des_w+=stock_tf[0]+'\001'
        print 'aaa:',des_w
        des_w+='\n'
        des_w = des_w.replace('\001\n','\n')
        ff2_out.write(des_w)

    ff1_out.close()
    ff2_out.close()
