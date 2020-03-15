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
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/知识点汇总1.csv', 'w', encoding="utf-8", newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["题目", "题目分词结果", "标签","数字标签", "知识点1", "知识点2", "知识点3"])
# 打开题库
f = open('C:/Users/27124/Desktop/毕业论文/dissertation/questions.csv', 'rb')
question = pd.read_csv(f, encoding='utf-8')
question["content"] = question["题目1"].map(str) + "，" + question["题目2"].map(str)  # 将包含的两列内容联合起来 第9列

#打开“带标签的知识点”文件，将内容存入一个map中备用
f_label = open('C:/Users/27124/Desktop/毕业论文/dissertation/带标签的知识点.csv', 'rb')
labelMap = pd.read_csv(f_label, encoding='utf-8')
labelDict={}
for index,row in labelMap.iterrows():
     labelDict[row[0]]=row[1]
labelDict["实数比较大小"]="代数"

numLabel={}
numLabel["代数"]=1
numLabel["复数"]=2
numLabel["概率"]=3
numLabel["函数"]=4
numLabel["集合"]=5
numLabel["计数原理"]=6
numLabel["简易逻辑"]=7
numLabel["解析几何"]=8
numLabel["平面几何"]=9
numLabel["矩阵与变换"]=10
numLabel["立体几何"]=11
numLabel["数列"]=12
numLabel["算法初步"]=13
numLabel["统计"]=14
numLabel["推理与证明"]=15
numLabel["相等关系与不等式"]=16
numLabel["向量几何"]=17
print(labelDict)
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
        if sims[i] != 0:
            sims[i] += weighList[i]
        simss.append(sims[i])  # 将每个句子对应的相似度放在列表中

    result = dict(zip(kownledge, simss))  # 将相似度和对应题目组合成为字典
    d_order = sorted(result.items(), key=lambda x: x[1], reverse=True)
    row_list = []
    row_list.append(txt_encode.decode('utf-8'))  # 题目
    row_list.append(doc_test_list2)  # 分词结果

    kown_lists = []
    for i in range(5):
        kown_lists.append(d_order[i][0])

    row_list.append(labelDict[kown_lists[0]])   #将第一个知识点的标签类型作为题目的类型
    row_list.append(numLabel[labelDict[kown_lists[0]]])   #将第一个知识点的标签类型作为题目的类型 的数字表示
    row_list.append(kown_lists[0])
    row_list.append(kown_lists[1])
    row_list.append(kown_lists[2])

    csv_writer.writerow(row_list)


def getword():
    return keyword