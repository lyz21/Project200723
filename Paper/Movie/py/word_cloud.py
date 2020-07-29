# encoding=utf-8
"""
@Time : 2020/7/24 22:24 
@Author : LiuYanZhe
@File : word_cloud.py 
@Software: PyCharm
@Description: 绘制词云图
先运行wordUtil.py中的get_words_list，获得分词文件，
再加载获得的分词文件，转化为一维列表，
依靠picUtil.py中的draw_word_cloud方法绘制词云图
"""
import pandas as pd
from collections import Counter
from Paper.Movie.util import wordUtil, picUtil

words = pd.read_csv('../data/words.csv').values.flatten()
word_dic = dict(Counter(words))
print('word_dic:', word_dic)
picUtil.draw_word_cloud(word_dic)
