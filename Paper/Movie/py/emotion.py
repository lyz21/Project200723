# encoding=utf-8
"""
@Time : 2020/7/25 12:29 
@Author : LiuYanZhe
@File : emotion.py 
@Software: PyCharm
@Description: 分析情感倾向
"""
from matplotlib.ticker import MultipleLocator
from snownlp import SnowNLP
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取到的数据为一维['评论1','评论2'...]
datas = pd.read_csv('../data/countryComment.csv')
# 将数据按时间排序
datas = datas.sort_values(by='评论日期')
print(datas)
# 评分统一格式
score = datas['评分'].values
score_list = []
for i in range(len(score)):
    if score[i] == 'comment-time':
        score_list.append(int(3))
    else:
        score_t = int(int(float(score[i])) / 10)
        score_list.append(score_t)
# 颜色列表
color_list = ['b', 'g', 'r', 'c', 'y']
div_c = [1, 2, 3, 4, 5]
# 画板
ax = plt.subplot(1, 1, 1)
# 为了先固定横坐标轴，画一组透明的点
date_all = datas['评论日期']
ax.scatter(date_all, np.ones(date_all.shape), c='w')
for c in div_c:
    print(c)
    datas_2 = datas.iloc[pd.Series(score_list).values == c].copy()
    # 评论内容
    data = datas_2['评论内容'].values

    # 认同人数
    up_num = datas_2['认同人数'].copy()
    up_num.iloc[list(datas_2['认同人数'] < 40)] = 40
    up_num = up_num.values
    # 时间
    date = datas_2['评论日期']
    # 依次判定每个评论的情感倾向
    emotion_score_list = []
    for comment in data:
        score = SnowNLP(comment).sentiments
        emotion_score_list.append(score)
    print('情感评分：', emotion_score_list)

    # 绘制散点图
    # ax.scatter(date, emotion_score_list, s=up_num, c=score_list, marker='o', alpha=0.4, lw=1)
    ax.scatter(date, emotion_score_list, s=up_num, c=color_list[c - 1], marker='o', alpha=0.4, lw=1,
               label=str(c * 10) + ' Points')

# 设置刻度倾斜和间隔
ax.xaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=80)
# 设置图例
lgnd = plt.legend(scatterpoints=1, fontsize=10)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]
lgnd.legendHandles[2]._sizes = [30]
lgnd.legendHandles[3]._sizes = [30]
lgnd.legendHandles[4]._sizes = [30]
# plt.show()
plt.savefig('../pic/emotion.png', dpi=400, bbox_inches='tight')
