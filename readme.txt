说明：
1、直接运行main_fun.py
    python main_fun.py corpus_name out_file_name1 out_file_name2
    corpus_name:语料文件名称，具体格式见baidu_20151014.txt
    out_file_name1:根据得分排序的结果
    out_file_name2:根据TF对stock进行排1中的结果，本结果是需要的结果

2、个别stock没有词向量，目前先做了保留。

3、word2vec_item_only.txt是从整个word2vec文件中读取的现阶段需要的stock的词向量，如果加入新的stock则运行selecct_word2vec.py即可。
