#-*-coding:GBK -*-
# ���ĳ������Ŀ��֪ʶ��
import jieba
from gensim import corpora,models,similarities
import pandas as pd
import re
import os
import csv

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

#�������ִʺ�Ľ��
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
    txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec",word)]
    all_doc_list .append(txt_cut1)


# �����Եľ��ӽ��зִ�
test_file = open('test.txt', 'r', encoding="utf-8")
test_content = test_file.read()
print("���Եľ�����", test_content)
doc_test_list=[word for word in jieba.cut(test_content) if word not in stopWords_list]
doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec",word)]
print("���Ծ��ӷִʵĽ���ǣ�", doc_test_list1)

# 2.�������Ͽ�
dictionary = corpora.Dictionary(all_doc_list)   # ��dictionary������ȡ�ʴ���bag-of-words)

dictionary.keys()   # �ʴ��������ֶ����дʽ����˱��
dictionary.token2id   # ������֮��Ķ�Ӧ��ϵ
print("�����ʵĸ���Ϊ", len(dictionary.keys()))
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]   # ʹ��doc2bow�������Ͽ�

doc_test_vec = dictionary.doc2bow(doc_test_list1)  # �����Ծ���Ҳת��Ϊϡ������

# 3. ���ƶȷ���
tfidf = models.TfidfModel(corpus)   # ʹ��TF-IDFģ�Ͷ����Ͽ⽨ģ
tfidf[doc_test_vec]  # ��ȡ�����ĵ��У�ÿ���ʵ�TF-IDFֵ
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))  # ��ÿ��Ŀ���ĵ������������ĵ������ƶ�
sims = index[tfidf[doc_test_vec]]

# �������

simss = []
for i in range(len(sims)):
    simss.append(sims[i])      # ��ÿ�����Ӷ�Ӧ�����ƶȷ����б���

print("���յĽ���ǣ��ı������ƶȶ�Ӧ����")
re = dict(zip(kownledge, simss))   # �����ƶȺͶ�Ӧ��Ŀ��ϳ�Ϊ�ֵ�
d_order=sorted(re.items(), key=lambda x:x[1], reverse=True)
for i in range(10):
    print(d_order[i])


'''
print("�����Ľ��")
re2 = sorted(enumerate(sims), key=lambda item: -item[1])   # �������ƶ�����
for i in range(3):
    print(re2[i])
'''










