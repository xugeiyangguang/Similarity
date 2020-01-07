import jieba
from gensim import corpora, models, similarities
import pandas as pd
import re
import os
import csv

# from dissertation.提取知识点及关键字 import getword

jieba.load_userdict("NewDict.txt")  # 加载用户自定义词典

# 从cvs文件读取数据
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)

kown_list = []
tmp = pd.read_csv('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点运行版.csv', encoding='utf-8')[["名称", "关键字"]]
kown_list.append(tmp)
kownledges = pd.concat(kown_list)

word = []
keyword = []
for index, row in kownledges.iterrows():
    word = row[1]
    tmp_words = word.split('，')
    for i in range(len(tmp_words)):
        keyword.append(tmp_words[i])

print("关键词(未经过分词)共有：",len(keyword))

# 1.分词

# 将停用词表从文件读出，并切分成一个数组备用
stopWords_dic = open('stop_words.txt', 'r', encoding="utf-8")  # 从文件中读入停用词
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()  # 转为list备用
stopWords_dic.close()

# 保存知识点的关键字分词后的结果   有的知识点关键词描述的有问题
doc_list = []  # 未分词
all_doc_list = []  # 以分词
kownledge = []  # 保存知识点名称
for index, row in kownledges.iterrows():
    # print(row["content"])
    kown = str(row["名称"]).encode("utf-8")
    kownledge.append(kown.decode("utf-8"))

    txt_encode = str(row["关键字"]).encode('utf-8')
    doc_list.append(txt_encode.decode('utf-8'))  # 将未切割的句子保存起来

    # 删除逗号
    txt_cut = [word for word in jieba.cut(txt_encode) if word not in stopWords_list]
    #去除停用词表的词语
 #   txt_cut = [word for word in jieba.cut(txt_encode) if word not in stopWords_list]  # 切词   切为列表
    #去除数字，字母表达式等与题目无关的变量等
    # txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|in|notin", word)]
    all_doc_list.append(txt_cut)

# 2.制作语料库
dictionary = corpora.Dictionary(all_doc_list)  # 用dictionary方法获取词袋（bag-of-words)

dictionary.keys()  # 词袋中用数字对所有词进行了编号
dictionary.token2id  # 编号与词之间的对应关系
print("特征词的个数为", len(dictionary.keys()))
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]  # 使用doc2bow制作语料库
tfidf = models.TfidfModel(corpus)  # 使用TF-IDF模型对语料库建模
