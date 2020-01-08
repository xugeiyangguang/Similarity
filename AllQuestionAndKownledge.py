# -*-coding:GBK -*-
# 将题库所有题目“questions1”和其相应的知识点输出到“知识点汇总中”
import jieba
from gensim import corpora, models, similarities
import pandas as pd
import re
import os
import csv
from dissertation.预处理 import *
from dissertation.分词 import fliterWords
#import sys.path.append(’引用模块的地址')


# 把所有题目中的关键词搜集起来
# csvfileKey = open('C:/Users/27124/Desktop/毕业论文/dissertation/题目的关键词.csv', 'w', encoding='utf-8', newline="")
# csv_writer = csv.writer(csvfileKey)
# print("开始输出所有的关键字到“题目的关键词”文件中")
# csv_writer.writerow(["关键词"])
# csv_writer.writerow(keyword)


# 打开写入的文件
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/知识点汇总.csv', 'w', encoding="utf-8", newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["题目", "题目分词结果", "知识点1", "知识点2", "知识点3"])
# 打开题库
f = open('C:/Users/27124/Desktop/毕业论文/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')
question["content"] = question["题目1"].map(str) + "," + question["题目2"].map(str)  # 将包含的两列内容联合起来 第9列
print("开始输出所有题目的相似考点到“知识点汇总中.csv”文件中")
for index, row in question.iterrows():
    txt_encode = row["content"].encode('utf-8')
    doc_test_list1 = fliterWords(txt_encode, keyword)


    #去除切词后重复的关键字
    doc_test_list2 = set(doc_test_list1)

    # 3. 相似度分析

    doc_test_vec = dictionary.doc2bow(doc_test_list2)  # 将测试句子也转换为稀疏向量
    tfidf[doc_test_vec]  # 获取测试文档中，每个词的TF-IDF值
    index = similarities.SparseMatrixSimilarity(tfidf[corpus],
                                                num_features=len(dictionary.keys()))  # 对每个目标文档，分析测试文档的相似度
    sims = index[tfidf[doc_test_vec]]

    simss = []
    for i in range(len(sims)):
        simss.append(sims[i])  # 将每个句子对应的相似度放在列表中

    result = dict(zip(kownledge, simss))  # 将相似度和对应题目组合成为字典
    d_order = sorted(result.items(), key=lambda x: x[1], reverse=True)
    row_list = []
    row_list.append(txt_encode.decode('utf-8'))  # 题目
    row_list.append(doc_test_list2)  # 分词结果
    kown_lists = []
    for i in range(5):
        kown_lists.append(d_order[i][0])

    row_list.append(kown_lists[0])
    row_list.append(kown_lists[1])
    row_list.append(kown_lists[2])

    csv_writer.writerow(row_list)


def getword():
    return keyword