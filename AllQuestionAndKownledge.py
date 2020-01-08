# -*-coding:GBK -*-
# �����������Ŀ��questions1��������Ӧ��֪ʶ���������֪ʶ������С�
import jieba
from gensim import corpora, models, similarities
import pandas as pd
import re
import os
import csv
from dissertation.Ԥ���� import *
from dissertation.�ִ� import fliterWords
#import sys.path.append(������ģ��ĵ�ַ')


# ��������Ŀ�еĹؼ����Ѽ�����
# csvfileKey = open('C:/Users/27124/Desktop/��ҵ����/dissertation/��Ŀ�Ĺؼ���.csv', 'w', encoding='utf-8', newline="")
# csv_writer = csv.writer(csvfileKey)
# print("��ʼ������еĹؼ��ֵ�����Ŀ�Ĺؼ��ʡ��ļ���")
# csv_writer.writerow(["�ؼ���"])
# csv_writer.writerow(keyword)


# ��д����ļ�
csvfile = open('C:/Users/27124/Desktop/��ҵ����/dissertation/֪ʶ�����.csv', 'w', encoding="utf-8", newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["��Ŀ", "��Ŀ�ִʽ��", "֪ʶ��1", "֪ʶ��2", "֪ʶ��3"])
# �����
f = open('C:/Users/27124/Desktop/��ҵ����/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')
question["content"] = question["��Ŀ1"].map(str) + "," + question["��Ŀ2"].map(str)  # ������������������������ ��9��
print("��ʼ���������Ŀ�����ƿ��㵽��֪ʶ�������.csv���ļ���")
for index, row in question.iterrows():
    txt_encode = row["content"].encode('utf-8')
    doc_test_list1 = fliterWords(txt_encode, keyword)


    #ȥ���дʺ��ظ��Ĺؼ���
    doc_test_list2 = set(doc_test_list1)

    # 3. ���ƶȷ���

    doc_test_vec = dictionary.doc2bow(doc_test_list2)  # �����Ծ���Ҳת��Ϊϡ������
    tfidf[doc_test_vec]  # ��ȡ�����ĵ��У�ÿ���ʵ�TF-IDFֵ
    index = similarities.SparseMatrixSimilarity(tfidf[corpus],
                                                num_features=len(dictionary.keys()))  # ��ÿ��Ŀ���ĵ������������ĵ������ƶ�
    sims = index[tfidf[doc_test_vec]]

    simss = []
    for i in range(len(sims)):
        simss.append(sims[i])  # ��ÿ�����Ӷ�Ӧ�����ƶȷ����б���

    result = dict(zip(kownledge, simss))  # �����ƶȺͶ�Ӧ��Ŀ��ϳ�Ϊ�ֵ�
    d_order = sorted(result.items(), key=lambda x: x[1], reverse=True)
    row_list = []
    row_list.append(txt_encode.decode('utf-8'))  # ��Ŀ
    row_list.append(doc_test_list2)  # �ִʽ��
    kown_lists = []
    for i in range(5):
        kown_lists.append(d_order[i][0])

    row_list.append(kown_lists[0])
    row_list.append(kown_lists[1])
    row_list.append(kown_lists[2])

    csv_writer.writerow(row_list)


def getword():
    return keyword