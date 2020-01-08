#-*-coding:GBK -*-
# 输出某单个题目的知识点
import jieba
from gensim import corpora,models,similarities
# from AllQuestionAndKownledge import keyword
#from .AllQuestionAndKownledge import keyword
import pandas as pd
import re
import os
import csv
from dissertation.预处理 import *
from dissertation.分词 import fliterWords

# 将测试的句子进行分词
test_file = open('C:/Users/27124/PycharmProjects/Similarity/dissertation/test.txt', 'r', encoding="utf-8")
test_content = test_file.read()
print("测试的句子是：", test_content)
#用户自定义的关键词文档要和知识点的关键词一样
doc_test_list2=fliterWords(test_content,keyword)

print("测试句子分词的结果是：", doc_test_list2)
doc_test_vec = dictionary.doc2bow(doc_test_list2)  # 将测试句子也转换为稀疏向量

# 3. 相似度分析
tfidf[doc_test_vec]  # 获取测试文档中，每个词的TF-IDF值
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))  # 对每个目标文档，分析测试文档的相似度
sims = index[tfidf[doc_test_vec]]

# 整理输出

simss = []
for i in range(len(sims)):
    simss.append(sims[i])      # 将每个句子对应的相似度放在列表中

print("最终的结果是（文本和相似度对应）：")
re = dict(zip(kownledge, simss))   # 将相似度和对应题目组合成为字典
d_order=sorted(re.items(), key=lambda x:x[1], reverse=True)
for i in range(10):
    print(d_order[i])


'''
print("排序后的结果")
re2 = sorted(enumerate(sims), key=lambda item: -item[1])   # 根据相似度排序
for i in range(3):
    print(re2[i])
'''










