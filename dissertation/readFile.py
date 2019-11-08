#-*-coding:GBK -*-
import pandas as pd
from dissertation.tf_idf import cut
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
jieba.load_userdict("NewDict.txt")   # �����û��Զ���ʵ�

#��ʾ������
pd.set_option('display.max_columns', None)
#��ʾ������

pd.set_option('display.max_rows', None)
#����value����ʾ����Ϊ100��Ĭ��Ϊ50
pd.set_option('max_colwidth', 100)
f=open('C:/Users/27124/Desktop/��ҵ����/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')

question["content"] = question["��Ŀ1"].map(str)+","+question["��Ŀ2"].map(str)  #������������������������ ��9��
# print(question.columns)    #��ʾ���е�����
# print(question.iloc[[10, 11], [9]])
corpus = []  #����ִʺ�Ľ��
for index, row in question.iterrows():
    # print(row["content"])
    txt_encode = row["content"].encode('utf-8')
    txt_cut = jieba.cut(txt_encode)  # �д�
    result = ' '.join(txt_cut)
    corpus.append(result)


# ��ͣ�ôʱ���ļ����������зֳ�һ�����鱸��
stopWords_dic = open('stop_words.txt', 'r')     # ���ļ��ж���ͣ�ô�
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # תΪlist����
stopWords_dic.close()

vector = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.6, stop_words=stopWords_list)
tf_idf = vector.fit_transform(corpus)    #���ı��еĴ���ת��Ϊ��Ƶ����

print(isinstance(tf_idf,list))
word_list = vector.get_feature_names()      # ��ȡ�ʴ�ģ�͵����д�
weight_list = tf_idf.toarray()

if __name__ == '__main__':
    for i in range(len(weight_list)):
        print("-------��", i + 1, "���ı��Ĵ���tf-idfȨ��------")
        for j in range(len(word_list)):
            print(word_list[j], weight_list[i][j])

