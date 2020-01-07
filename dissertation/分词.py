import jieba
import re

def fliterWords(str,keyword):
    doc_test_list = [word for word in jieba.cut(str) if word in keyword]
    doc_test_list1 = [word for word in doc_test_list if
                      re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec", word)]
    # doc_test_list=[word for word in jieba.cut(test_content) if word not in stopWords_list]
    # doc_test_list11 = [word for word in doc_test_list if word in keyword]
    # doc_test_list1 = [word for word in doc_test_list if re.match("([\u4E00-\u9FA5]+)|sin|cos|log|cot|lim|dx|parallel|overrightarrow|vec",word)]
    # doc_test_list2 = set(doc_test_list1)

    doc_test_list2 = set(doc_test_list1)
    return doc_test_list2
