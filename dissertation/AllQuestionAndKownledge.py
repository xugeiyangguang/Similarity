#-*-coding:GBK -*-
# 将题库所有题目“questions1”和其相应的知识点输出到“知识点汇总中”
import jieba
from gensim import corpora,models,similarities
import pandas as pd
import re
import os
import csv

# 将从思维导图导出的文件转换为为其他程序执行的知识点列表文件“初等数学知识点运行版”
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点运行版.csv', 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["名称", "关键字", "路径"])

ff=open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点.csv', 'rb')
questionn = pd.read_csv(ff, encoding='utf-8')
questionn.drop([0,1])
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
            list_tmp.append(words)
            list_tmp.append(key)
            csv_writer.writerow(list_tmp)  # 将三者保写入文件中
print("一共包含知识点：",len(kownledge_listt))


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
# 1.分词

# 将停用词表从文件读出，并切分成一个数组备用
stopWords_dic = open('stop_words.txt', 'r',encoding="utf-8")     # 从文件中读入停用词
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # 转为list备用
stopWords_dic.close()

#保存知识点分词后的结果
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
    txt_cut1 = [word for word in txt_cut if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx",word)]
    all_doc_list .append(txt_cut1)

# 2.制作语料库
dictionary = corpora.Dictionary(all_doc_list)   # 用dictionary方法获取词袋（bag-of-words)

dictionary.keys()   # 词袋中用数字对所有词进行了编号
dictionary.token2id   # 编号与词之间的对应关系
print("特征词的个数为", len(dictionary.keys()))
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]   # 使用doc2bow制作语料库

# 3. 相似度分析
tfidf = models.TfidfModel(corpus)   # 使用TF-IDF模型对语料库建模

# 打开写入的文件
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/知识点汇总.csv', 'w', encoding="utf-8", newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["题目", "题目分词结果", "知识点1", "知识点2", "知识点3"])
# 打开题库
f=open('C:/Users/27124/Desktop/毕业论文/dissertation/questions1.csv', 'rb')
question = pd.read_csv(f, encoding='gb18030')
question["content"] = question["题目1"].map(str)+","+question["题目2"].map(str)  #将包含的两列内容联合起来 第9列
for index, row in question.iterrows():
    txt_encode = row["content"].encode('utf-8')
    doc_test_list=[word for word in jieba.cut(txt_encode) if word not in stopWords_list]
    doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log",word)]

    doc_test_vec = dictionary.doc2bow(doc_test_list1)  # 将测试句子也转换为稀疏向量

    tfidf[doc_test_vec]  # 获取测试文档中，每个词的TF-IDF值
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))  # 对每个目标文档，分析测试文档的相似度
    sims = index[tfidf[doc_test_vec]]

    simss = []
    for i in range(len(sims)):
        simss.append(sims[i])  # 将每个句子对应的相似度放在列表中

    result = dict(zip(kownledge, simss))  # 将相似度和对应题目组合成为字典
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


