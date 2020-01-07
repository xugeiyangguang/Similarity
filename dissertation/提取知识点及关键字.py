import csv

import pandas as pd

# 将从思维导图导出的文件转换为为其他程序执行的知识点列表文件“初等数学知识点运行版”
# 之后都不用运行
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点运行版.csv', 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["名称", "关键字"])

ff = open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点.csv', 'rb')
questionn = pd.read_csv(ff, encoding='utf-8')
questionn.drop([0, 1])

keyword = []  # 保存为关键字
with open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点1.csv', 'r', encoding='utf-8') as f1:
    reader = csv.reader(f1)
    dictt = {}
    kownledge_listt = set()
    for i, row in enumerate(reader):
        if i > 0:
            value = ""  # 知识点名称
            count = 0
            #   key = ""   # 路径
            words = ""  # 关键字

            for j, tmp in enumerate(row):
                if tmp != "":
                    words = tmp
                    tmp_words = words.split('，')
                    for i in range(len(tmp_words)):
                        keyword.append(tmp_words[i])
                    value = row[j + 1]
                    break
            kownledge_listt.add(value)
            list_tmp = []
            list_tmp.append(value)
            list_tmp.append(words)
            csv_writer.writerow(list_tmp)  # 将2者保写入文件中

        #   dictt[value] = key  # 将知识点名称，路径保存为字典

print("一共包含知识点：", len(kownledge_listt))

def getword():
    return keyword