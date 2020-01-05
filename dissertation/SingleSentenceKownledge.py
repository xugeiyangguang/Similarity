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


jieba.load_userdict("NewDict.txt")   # 加载用户自定义词典

#从cvs文件读取数据
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)

'''
# 将多个知识点列表读取到一个列表中
path = 'C:/Users/27124/Desktop/毕业论文/dissertation/知识点列表/'
files = os.listdir(path)
files_csv = list(filter(lambda x: x[-4:]=='.csv', files))

kown_list = []
for file in files_csv:
    tmp = pd.read_csv(path+file, encoding='gbk')[["名称", "关键字"]]
    kown_list.append(tmp)

kownledges = pd.concat(kown_list)
'''
kown_list = []
tmp = pd.read_csv('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点运行版.csv', encoding='utf-8')[["名称", "关键字"]]
kown_list.append(tmp)
kownledges = pd.concat(kown_list)

keyword = []       # 保存为关键字
with open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点.csv', 'r', encoding='utf-8') as f1:
    reader = csv.reader(f1)
    dictt = {}
    kownledge_listt = set()
    for i,row in enumerate(reader):
        if i>0:
            value = ""  # 知识点名称
            count = 0
            key = ""   # 路径
            words = ""  # 关键字

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
            dictt[value] = key  # 将知识点名称，路径保存为字典
            kownledge_listt.add(value)
            list_tmp = []
            list_tmp.append(value)
            tmp_words = words.split('，')
            for i in range(len(tmp_words)):
                keyword.append(tmp_words[i])
            list_tmp.append(key)
        #    csv_writer.writerow(list_tmp)  # 将三者保写入文件中
print("一共包含知识点：",len(kownledge_listt))

# 1.分词

# 将停用词表从文件读出，并切分成一个数组备用
stopWords_dic = open('stop_words.txt', 'r',encoding="utf-8")     # 从文件中读入停用词
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # 转为list备用
stopWords_dic.close()

#保存题库分词后的结果
doc_list = []   # 未分词
all_doc_list = []   # 以分词
kownledge = []   # 保存知识点
for index, row in kownledges.iterrows():
    # print(row["content"])
    kown = str(row["名称"]).encode("utf-8")
    kownledge.append(kown.decode("utf-8"))

    txt_encode = str(row["关键字"]).encode('utf-8')
    doc_list.append(txt_encode.decode('utf-8'))    # 将未切割的句子保存起来
    txt_cut = [word for word in jieba.cut(txt_encode) if word not in stopWords_list]  # 切词   切为列表
    txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec",word)]
    all_doc_list .append(txt_cut1)


# 将测试的句子进行分词
test_file = open('test.txt', 'r', encoding="utf-8")
test_content = test_file.read()
print("测试的句子是", test_content)
doc_test_list=[word for word in jieba.cut(test_content) if word not in stopWords_list]
doc_test_list11 = [word for word in doc_test_list if word in keyword]
doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec",word)]
doc_test_list2 = set(doc_test_list1)
print("测试句子分词的结果是：", doc_test_list2)

# 2.制作语料库
dictionary = corpora.Dictionary(all_doc_list)   # 用dictionary方法获取词袋（bag-of-words)

dictionary.keys()   # 词袋中用数字对所有词进行了编号
dictionary.token2id   # 编号与词之间的对应关系
print("特征词的个数为", len(dictionary.keys()))
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]   # 使用doc2bow制作语料库

doc_test_vec = dictionary.doc2bow(doc_test_list2)  # 将测试句子也转换为稀疏向量

# 3. 相似度分析
tfidf = models.TfidfModel(corpus)   # 使用TF-IDF模型对语料库建模
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










