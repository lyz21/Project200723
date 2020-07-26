# encoding=utf-8
"""
@Time : 2020/7/25 19:23 
@Author : LiuYanZhe
@File : lda_test2.py 
@Software: PyCharm
@Description: 测试LDA主题分类模型
"""
# 使用gensim中的lda库
from gensim import corpora
from gensim.models import doc2vec, ldamodel
from Paper.Movie.util import wordUtil
import pandas as pd

# 得到分好词的二维数组
words_list = wordUtil.get_words_list2()
print('words_list:', words_list)
# 得到词向量（所有词去重，作为索引）
dictionary = corpora.Dictionary(words_list)
print('dictionary:', dictionary)
print('dictionary[0]:', dictionary[0])
# 统计每条文本中每个词的词频 (0,1),下标为0的词出现一次
corpus = [dictionary.doc2bow(text) for text in words_list]
print('corpus:', corpus)
lda = ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
print('print_topic(10, topn=5):', lda.print_topic(10, topn=5))  # 打印第10个主题的前五个词
print(lda.num_topics)
print('print_topics(num_topics=20, num_words=5):', lda.print_topics(num_topics=20, num_words=30))  # 打印所有主题
