from gensim import corpora, models, similarities
import jieba
text1 = '小明喜欢吃水果'
text2 = '苹果是水果'
texts = [text1, text2]
keyword = '小明喜欢吃苹果'
texts = [jieba.lcut(text) for text in texts]
dictionary = corpora.Dictionary(texts)
num_features = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
new_vec = dictionary.doc2bow(jieba.lcut(keyword))
# 相似度计算
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features)
print('\nTF-IDF模型的稀疏向量集：')
for i in tfidf[corpus]:
    print(i)
print('\nTF-IDF模型的keyword稀疏向量：')
print(tfidf[new_vec])
print('\n相似度计算：')
sim = index[tfidf[new_vec]]
for i in range(len(sim)):
    print('第', i+1, '句话的相似度为：', sim[i])
