# -*-coding:GBK -*-
# ���ĳ������Ŀ��֪ʶ��
import jieba
from gensim import corpora, models, similarities
# from AllQuestionAndKownledge import keyword
# from .AllQuestionAndKownledge import keyword
import pandas as pd
import re
import os
import csv

from pip._vendor.distlib.compat import raw_input

from dissertation.Ԥ���� import *
from dissertation.�ִ� import fliterWords

# �����Եľ��ӽ��зִ�
test_file = open('C:/Users/27124/PycharmProjects/Similarity/dissertation/test.txt', 'r', encoding="utf-8")
test_content = test_file.read()
# test_content = raw_input("�����룺")
print("���Եľ����ǣ�", test_content)
# �û��Զ���Ĺؼ����ĵ�Ҫ��֪ʶ��Ĺؼ���һ��
doc_test_list2 = fliterWords(test_content, keyword)

print("���Ծ��ӷִʵĽ���ǣ�", doc_test_list2)
doc_test_vec = dictionary.doc2bow(doc_test_list2)  # �����Ծ���Ҳת��Ϊϡ������

# 3. ���ƶȷ���
tfidf[doc_test_vec]  # ��ȡ�����ĵ��У�ÿ���ʵ�TF-IDFֵ
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))  # ��ÿ��Ŀ���ĵ������������ĵ������ƶ�
sims = index[tfidf[doc_test_vec]]

# �������

simss = []
for i in range(len(sims)):
    if sims[i] != 0:
        sims[i] += weighList[i]
    simss.append(sims[i])  # ��ÿ�����Ӷ�Ӧ�����ƶȷ����б���

print("���յĽ���ǣ��ı������ƶȶ�Ӧ����")
re = dict(zip(kownledge, simss))  # �����ƶȺͶ�Ӧ��Ŀ��ϳ�Ϊ�ֵ�
d_order = sorted(re.items(), key=lambda x: x[1], reverse=True)
for i in range(10):
    print(d_order[i], end="")
    print(kownDict[(d_order[i][0]).encode("utf-8")])

baseKownledge = []
for i in range(3):
    baseKownledge.append(d_order[i][0])

print(baseKownledge)
'''
print("�����Ľ��")
re2 = sorted(enumerate(sims), key=lambda item: -item[1])   # �������ƶ�����
for i in range(3):
    print(re2[i])
'''

