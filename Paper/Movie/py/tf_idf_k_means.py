# encoding=utf-8
"""
@Time : 2020/7/26 19:07 
@Author : LiuYanZhe
@File : tf_idf_k_means.py 
@Software: PyCharm
@Description: TF-IDF词向量化，k-means聚类,数据使用我和我的祖国+红海行动
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from Paper.Movie.util import wordUtil

# 设置显示pd所有行
# pd.set_option('display.max_rows', None)  # 行
# pd.set_option('display.max_columns', None)  # 列
# 读取文件
country = pd.read_excel('../data/我和我的祖国豆瓣影评.xlsx')
# red = pd.read_excel('../data/红海行动豆瓣影评.xlsx')
# 填充缺失值
country = country.fillna(-1)
# red = red.fillna(-1)
# 去除信息不全的
# country = country.iloc[
#     list((country['评论人所在城市'] != '无') & (country['评论人所在城市'] != -1) & (country['评分'] != 'comment-time'))]
# country = country.iloc[
#     list((country['评论人所在城市'] != '无') & (country['评论人所在城市'] != -1))]
# red = red.iloc[list((red['评论人所在城市'] != '无') & (red['评论人所在城市'] != -1))]
# 提取需要的信息
country = country.loc[:, ['评论内容', '评论人所在城市', '评分']]
# red = red.loc[:, ['评论内容', '评论人所在城市']]
# 合并
# data = pd.concat([country, red], axis=0)
data = country
data = data.reset_index(drop=True)
print(data)
# 评论转为一维，准备向量化
contens = []
for c in data['评论内容'].values:
    contens.append(c)
print('contens:', contens)
# 构建语料库，计算文档的TF-IDF矩阵，输入为一维列表
transformer = TfidfVectorizer()
tfidt = transformer.fit_transform(contens)
# TF-IDF以稀疏矩阵的形式存储，将TF-IDF转化为数组形式，文档-词矩阵
word_vectors = tfidt.toarray()
print('word_vectors:\n', word_vectors)
# 对word_vectors进行k均值聚类      参数聚类数目n_clusters，随机种子random_state = 0。
kmeans = KMeans(n_clusters=3, random_state=0).fit(word_vectors)
# 聚类得到的类别
labels_list = kmeans.labels_
data['label'] = labels_list
data.to_csv('../data/data_label.csv', index=False)
# 将类别转为颜色
# label_color = data['label'].copy()
# label_color.iloc[label_color.values == 0] = 'r'
# label_color.iloc[label_color.values == 1] = 'c'
# print(data.head(50))
# PCA降维
pca = PCA(n_components=2)
pca.fit(word_vectors)
pca_results = pca.fit_transform(word_vectors)
print(pca_results)
'''获得情感分值'''
comment_list = data['评论内容'].values
print(comment_list)
comments_score = wordUtil.get_emotion_score(comment_list)
print(comments_score)
# 按比例扩大情感值（否则点太小）
comments_score = pd.Series(comments_score)
comments_score *= 100
comments_score = comments_score * comments_score * comments_score * comments_score * comments_score
comments_score /= 100000000
comments_score.iloc[comments_score.values < 5] = 5
comments_score.iloc[(comments_score.values >= 5) & (comments_score.values < 10)] = 10
comments_score.iloc[(comments_score.values >= 10) & (comments_score.values < 20)] = 20
# comments_score.iloc[(comments_score.values >= 0.6) & (comments_score.values < 0.8)] = 65
# comments_score.iloc[(comments_score.values >= 0.8) & (comments_score.values < 1.1)] = 85
print(comments_score)
# 获得评分并转换格式
# sc = data['评分'].values
# sc = pd.Series(sc)
# sc = sc.astype('float')
# 计算每一类的得分均值
data_m = data.iloc[list(data['评分'] != 'comment-time')]
score_mean1 = data_m.iloc[list(data_m['label'] == 0), 2].astype('float').mean()
score_mean2 = data_m.iloc[list(data_m['label'] == 1), 2].astype('float').mean()
score_mean3 = data_m.iloc[list(data_m['label'] == 2), 2].astype('float').mean()
print('score_mean1:', score_mean1)

# 绘制降维后的分类结果
plt.scatter(pca_results[:, 0], pca_results[:, 1], alpha=0.4, lw=1.2, s=comments_score, c=data['label'])
# 绘制箭头
plt.annotate('The average score is ' + str(round(score_mean1, 2)), xy=(-0.1, 0.4), xytext=(0, 0.8),
             arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
plt.annotate('The average score is ' + str(round(score_mean2, 2)), xy=(0, 0), xytext=(0.1, 0.3),
             arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
plt.annotate('The average score is ' + str(round(score_mean3, 2)), xy=(0.5, 0.17), xytext=(0.4, 0.5),
             arrowprops=dict(facecolor='red', alpha=0.5, shrink=0.05))  # 添加标注（箭头）（指向位置，文字位置，颜色，透明度，收缩比例）
plt.savefig('../pic/k-means.png', dpi=400, bbox_inches='tight')
plt.show()
