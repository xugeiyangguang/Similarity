#-*-coding:GBK -*-
import pandas as pd
from dissertation.tf_idf import cut
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
jieba.load_userdict("NewDict.txt")   # 加载用户自定义词典

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行

pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)
f=open('C:/Users/27124/Desktop/毕业论文/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')

question["content"] = question["题目1"].map(str)+","+question["题目2"].map(str)  #将包含的两列内容联合起来 第9列
# print(question.columns)    #显示所有的列名
# print(question.iloc[[10, 11], [9]])
corpus = []  #保存分词后的结果
for index, row in question.iterrows():
    # print(row["content"])
    txt_encode = row["content"].encode('utf-8')
    txt_cut = jieba.cut(txt_encode)  # 切词
    result = ' '.join(txt_cut)
    corpus.append(result)


# 将停用词表从文件读出，并切分成一个数组备用
stopWords_dic = open('stop_words.txt', 'r')     # 从文件中读入停用词
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # 转为list备用
stopWords_dic.close()

vector = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.6, stop_words=stopWords_list)
tf_idf = vector.fit_transform(corpus)    #将文本中的词语转换为词频矩阵

print(isinstance(tf_idf,list))
word_list = vector.get_feature_names()      # 获取词袋模型的所有词
weight_list = tf_idf.toarray()

if __name__ == '__main__':
    for i in range(len(weight_list)):
        print("-------第", i + 1, "段文本的词语tf-idf权重------")
        for j in range(len(word_list)):
            print(word_list[j], weight_list[i][j])

