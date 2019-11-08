#-*-coding:GBK -*-
# ����������Ŀ�����ƶ�
import jieba
from gensim import corpora,models,similarities
import pandas as pd
import re

jieba.load_userdict("NewDict.txt")   # �����û��Զ���ʵ�

#��cvs�ļ���ȡ����
#��ʾ������
pd.set_option('display.max_columns', None)
#��ʾ������
pd.set_option('display.max_rows', None)
#����value����ʾ����Ϊ100��Ĭ��Ϊ50
pd.set_option('max_colwidth', 100)
f=open('C:/Users/27124/Desktop/��ҵ����/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')


question["content"] = question["��Ŀ1"].map(str)+","+question["��Ŀ2"].map(str)  #������������������������ ��9��


# 1.�ִ�

# ��ͣ�ôʱ���ļ����������зֳ�һ�����鱸��
stopWords_dic = open('stop_words.txt', 'r',encoding="utf-8")     # ���ļ��ж���ͣ�ô�
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # תΪlist����
stopWords_dic.close()

#�������ִʺ�Ľ��
doc_list = []   # δ�ִ�
all_doc_list = []   # �Էִ�
for index, row in question.iterrows():
    # print(row["content"])
    txt_encode = row["content"].encode('utf-8')
    doc_list.append(txt_encode.decode('utf-8'))    # ��δ�и�ľ��ӱ�������
    txt_cut = [word for word in jieba.cut(txt_encode) if word not in stopWords_list]  # �д�   ��Ϊ�б�
    txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log",word)]
    all_doc_list .append(txt_cut1)


# �����Եľ��ӽ��зִ�
test_file = open('test.txt', 'r', encoding="utf-8")
test_content = test_file.read()
print("���Եľ�����", test_content)
doc_test_list=[word for word in jieba.cut(test_content) if word not in stopWords_list]
doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log",word)]
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
re = dict(zip(doc_list, simss))   # �����ƶȺͶ�Ӧ��Ŀ��ϳ�Ϊ�ֵ�
d_order=sorted(re.items(), key=lambda x:x[1], reverse=True)
for i in range(3):
    print(d_order[i])

'''
print("�����Ľ��")
re2 = sorted(enumerate(sims), key=lambda item: -item[1])   # �������ƶ�����
for i in range(3):
    print(re2[i])
'''









