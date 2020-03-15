"""
jieba分词测试
"""
import jieba

#全模式
test1 = jieba.cut("在这里，你可以畅所欲言，你可以以一种新颖有趣的方式了解你所不了解的。", cut_all=True)
print("全模式: " + "| ".join(test1))

#精确模式
test2 = jieba.cut("在这里，你可以畅所欲言，你可以以一种新颖有趣的方式了解你所不了解的。", cut_all=False)
print("精确模式: " + "| ".join(test2))

#搜索引擎模式
test3= jieba.cut_for_search("在这里，你可以畅所欲言，你可以以一种新颖有趣的方式了解你所不了解的。")
print("搜索引擎模式:" + "| ".join(test3))
