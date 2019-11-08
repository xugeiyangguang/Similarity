#-*-coding:GBK -*-
# �����������Ŀ��questions1��������Ӧ��֪ʶ���������֪ʶ������С�
import jieba
from gensim import corpora,models,similarities
import pandas as pd
import re
import os
import csv

# ����˼ά��ͼ�������ļ�ת��ΪΪ��������ִ�е�֪ʶ���б��ļ���������ѧ֪ʶ�����а桱
csvfile = open('C:/Users/27124/Desktop/��ҵ����/dissertation/������ѧ֪ʶ�����а�.csv', 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["����", "�ؼ���", "·��"])

ff=open('C:/Users/27124/Desktop/��ҵ����/dissertation/������ѧ֪ʶ��.csv', 'rb')
questionn = pd.read_csv(ff, encoding='utf-8')
questionn.drop([0,1])
with open('C:/Users/27124/Desktop/��ҵ����/dissertation/������ѧ֪ʶ��.csv', 'r', encoding='utf-8') as f1:
    reader = csv.reader(f1)
    dictt = {}
    kownledge_listt = set()
    for i,row in enumerate(reader):
        if i>0:
            value = ""  # ֪ʶ������
            count = 0
            key = ""   # ·��
            words = ""  # �ؼ���

            for j,tmp in enumerate(row):
                t = row[j]
                if j<len(row)-1 and row[j+1] != "":
                    if key == '':
                        key = tmp
                    else:
                        key = key + "-->" + tmp

                else:
                    words = tmp
                    value = row[j-1]
                    break
            dictt[value] = key  # ��֪ʶ�����ƣ�·������Ϊ�ֵ�
            kownledge_listt.add(value)
            list_tmp = []
            list_tmp.append(value)
            list_tmp.append(words)
            list_tmp.append(key)
            csv_writer.writerow(list_tmp)  # �����߱�д���ļ���
print("һ������֪ʶ�㣺",len(kownledge_listt))


jieba.load_userdict("NewDict.txt")   # �����û��Զ���ʵ�

#��cvs�ļ���ȡ����
#��ʾ������
pd.set_option('display.max_columns', None)
#��ʾ������
pd.set_option('display.max_rows', None)
#����value����ʾ����Ϊ100��Ĭ��Ϊ50
pd.set_option('max_colwidth', 100)

'''
# �����֪ʶ���б��ȡ��һ���б���
path = 'C:/Users/27124/Desktop/��ҵ����/dissertation/֪ʶ���б�/'
files = os.listdir(path)
files_csv = list(filter(lambda x: x[-4:]=='.csv', files))

kown_list = []
for file in files_csv:
    tmp = pd.read_csv(path+file, encoding='gbk')[["����", "�ؼ���"]]
    kown_list.append(tmp)

kownledges = pd.concat(kown_list)
'''
kown_list = []
tmp = pd.read_csv('C:/Users/27124/Desktop/��ҵ����/dissertation/������ѧ֪ʶ�����а�.csv', encoding='utf-8')[["����", "�ؼ���"]]
kown_list.append(tmp)
kownledges = pd.concat(kown_list)
# 1.�ִ�

# ��ͣ�ôʱ���ļ����������зֳ�һ�����鱸��
stopWords_dic = open('stop_words.txt', 'r',encoding="utf-8")     # ���ļ��ж���ͣ�ô�
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # תΪlist����
stopWords_dic.close()

#����֪ʶ��ִʺ�Ľ��
doc_list = []   # δ�ִ�
all_doc_list = []   # �Էִ�
kownledge = []   # ����֪ʶ��
for index, row in kownledges.iterrows():
    # print(row["content"])
    kown = str(row["����"]).encode("utf-8")
    kownledge.append(kown.decode("utf-8"))

    txt_encode = str(row["�ؼ���"]).encode('utf-8')
    doc_list.append(txt_encode.decode('utf-8'))    # ��δ�и�ľ��ӱ�������
    txt_cut = [word for word in jieba.cut(txt_encode) if word not in stopWords_list]  # �д�   ��Ϊ�б�
    txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx",word)]
    all_doc_list .append(txt_cut1)

# 2.�������Ͽ�
dictionary = corpora.Dictionary(all_doc_list)   # ��dictionary������ȡ�ʴ���bag-of-words)

dictionary.keys()   # �ʴ��������ֶ����дʽ����˱��
dictionary.token2id   # ������֮��Ķ�Ӧ��ϵ
print("�����ʵĸ���Ϊ", len(dictionary.keys()))
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]   # ʹ��doc2bow�������Ͽ�

# 3. ���ƶȷ���
tfidf = models.TfidfModel(corpus)   # ʹ��TF-IDFģ�Ͷ����Ͽ⽨ģ

# ��д����ļ�
csvfile = open('C:/Users/27124/Desktop/��ҵ����/dissertation/֪ʶ�����.csv', 'w', encoding="utf-8", newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["��Ŀ", "��Ŀ�ִʽ��", "֪ʶ��1", "֪ʶ��2", "֪ʶ��3"])
# �����
f=open('C:/Users/27124/Desktop/��ҵ����/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')
question["content"] = question["��Ŀ1"].map(str)+","+question["��Ŀ2"].map(str)  #������������������������ ��9��
for index, row in question.iterrows():
    txt_encode = row["content"].encode('utf-8')
    doc_test_list=[word for word in jieba.cut(txt_encode) if word not in stopWords_list]
    doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log",word)]

    doc_test_vec = dictionary.doc2bow(doc_test_list1)  # �����Ծ���Ҳת��Ϊϡ������

    tfidf[doc_test_vec]  # ��ȡ�����ĵ��У�ÿ���ʵ�TF-IDFֵ
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))  # ��ÿ��Ŀ���ĵ������������ĵ������ƶ�
    sims = index[tfidf[doc_test_vec]]

    simss = []
    for i in range(len(sims)):
        simss.append(sims[i])  # ��ÿ�����Ӷ�Ӧ�����ƶȷ����б���

    result = dict(zip(kownledge, simss))  # �����ƶȺͶ�Ӧ��Ŀ��ϳ�Ϊ�ֵ�
    d_order = sorted(result.items(), key=lambda x: x[1], reverse=True)
    row_list=[]
    row_list.append(txt_encode.decode('utf-8'))
    row_list.append(doc_test_list1)
    kown_lists = []
    for i in range(5):
        kown_lists.append(d_order[i][0])
    re_dict = {}
    for i in range(len(kown_lists)):
        for j in range(len(kown_lists)):
            if i!=j:

                if dictt[kown_lists[i]].startswith(dictt[kown_lists[j]]):
                    re_dict[kown_lists[j]] = 1
                elif dictt[kown_lists[j]].startswith(dictt[kown_lists[i]]):
                    re_dict[kown_lists[i]] = 1
                else:
                    re_dict[kown_lists[j]] = 0
                    re_dict[kown_lists[i]] = 0
    for i,j in enumerate(kown_lists):

        if re_dict[j]==1:
            del kown_lists[i]
    for i in range(3):
        row_list.append(kown_lists[i])
    csv_writer.writerow(row_list)


