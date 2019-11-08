import pandas as pd
import csv
# 将从思维导图导出的文件转换为为其他程序执行的知识点列表文件“初等数学知识点运行版”
csvfile = open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点运行版.csv', 'w', encoding='utf-8', newline="")
csv_writer = csv.writer(csvfile)
csv_writer.writerow(["名称", "关键字", "路径"])

# 存放从xmind中导入的无重复知识点的表格
csvfile1 = open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点无重复版.csv', 'w', encoding='utf-8', newline="")
csv_writer1 = csv.writer(csvfile1)
csv_writer1.writerow(["名称", "路径"])

f=open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点.csv', 'rb')
question = pd.read_csv(f, encoding='utf-8')
question.drop([0,1])

with open('C:/Users/27124/Desktop/毕业论文/dissertation/初等数学知识点.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    dict = {}
    kownledge_list = set()
    for i,row in enumerate(reader):
        if i>0:
            value = ""  # 知识点名称
            count = 0
            key = ""   # 路径
            words = ""  # 关键字

            for j,tmp in enumerate(row):
                t = row[j]
                if j<len(row)-1 and row[j+1] != "":
                    if value == '':
                         value = tmp
                    else:
                        value = value + "-->" + tmp

                else:
                    words = tmp
                    key = row[j-1]
                    break
            dict[key] = value  # 将知识点名称，路径保存为字典
            kownledge_list.add(key)
            list_tmp = []
            list_tmp.append(key)
            list_tmp.append(words)
            list_tmp.append(value)
            csv_writer.writerow(list_tmp)  # 将三者保写入文件中

    #写入无重复的知识点文件
    for i in kownledge_list:
        list_tmp1 = []
        list_tmp1.append(i)
        list_tmp1.append(dict[i])
        csv_writer1.writerow(list_tmp1)
print("一共包含知识点：",len(kownledge_list))



