# encoding=utf-8
"""
@Time : 2020/7/24 21:53 
@Author : LiuYanZhe
@File : wordUtil.py 
@Software: PyCharm
@Description: 处理评论相关的工具类
"""
import pandas as pd
from snownlp import SnowNLP
from textrank4zh import TextRank4Keyword
from collections import Counter


# 获取评论划分后的词，返回list类型的一维列表
def get_words_list(path='../data/countryComment.csv'):
    tr4w = TextRank4Keyword()
    # 获取评论
    comments = pd.read_csv(path)['评论内容'].values
    # 划分分词
    word_list = []
    for comment in comments:
        tr4w.analyze(text=comment)
        words = tr4w.words_all_filters
        words = sum(words, [])  # 二维转一维
        word_list.append(words)
        print(word_list)
    words = sum(word_list, [])
    words = pd.DataFrame(words)
    words.to_csv('../data/words.csv', index=False)
    print('words.csv文件保存成功！')
    return words


# 获取评论划分后的词，返回list类型的二维列表
def get_words_list2(path='../data/countryComment.csv'):
    tr4w = TextRank4Keyword()
    # 获取评论
    comments = pd.read_csv(path)['评论内容'].values
    # 划分分词
    word_list = []
    for comment in comments:
        tr4w.analyze(text=comment)
        words = tr4w.words_all_filters
        words = sum(words, [])  # 二维转一维
        word_list.append(words)
        # print(word_list)
    return word_list
# 传入一维数组，得到一维的情感分值
def get_emotion_score(list_data):
    emotion_score_list = []
    for comment in list_data:
        score = SnowNLP(comment).sentiments
        emotion_score_list.append(score)
    return emotion_score_list


if __name__ == '__main__':
    # words = get_words_list()
    # words = pd.read_csv('../data/words.txt').values.flatten()
    # word_dic = Counter(words)
    # print(word_dic)
    get_words_list2()
