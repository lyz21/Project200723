# encoding=utf-8
"""
@Time : 2020/7/26 12:49 
@Author : LiuYanZhe
@File : score_byarea.py 
@Software: PyCharm
@Description: 按喜好电影地区不同分析评分
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_cn = pd.read_csv('../data/country_area.csv')
data_red = pd.read_csv('../data/red_area.csv')
data_three = pd.read_csv('../data/three_area.csv')
cn_list = []
red_list = []
th_list = []
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in x:
    # 分别获取分数
    sc_cn = data_cn.iloc[list(data_cn['国产电影数量'] == i), 0].values
    sc_red = data_red.iloc[list(data_red['国产电影数量'] == i), 0].values
    sc_th = data_three.iloc[list(data_three['国产电影数量'] == i), 0].values
    # 计算平均分
    if len(sc_cn) == 0:
        mean_cn = 0
    else:
        mean_cn = np.mean(sc_cn)
        cn_list.append(mean_cn)
    if len(sc_red) == 0:
        mean_red = 0
    else:
        mean_red = np.mean(sc_red)
        red_list.append(mean_red)
    if len(sc_th) == 0:
        mean_th = 0
    else:
        mean_th = np.mean(sc_th)
        th_list.append(mean_th)
    # 存储到list

# 绘图
ax = plt.subplot(1, 1, 1)
ax.plot(list(range(1, len(cn_list) + 1)), cn_list, color='r', label='My People,My Country')
ax.plot(list(range(1, len(red_list) + 1)), red_list, color='g', label='OPERATION RED SEA')
ax.plot(list(range(1, len(th_list) + 1)), th_list, color='y', label='Three Billboards Outside Ebbing, Missouri')
# 折线平滑
window_length = 3  # 窗口长度，越大平滑越明显
polyorder = 1  # 多项式拟合的阶数，越小平滑越明显
ax.plot(list(range(1, len(cn_list) + 1)), savgol_filter(cn_list, window_length, polyorder), color='r', linestyle='--')
ax.plot(list(range(1, len(red_list) + 1)), savgol_filter(red_list, window_length, polyorder), color='g',
        linestyle='--')
ax.plot(list(range(1, len(th_list) + 1)), savgol_filter(th_list, window_length, polyorder), color='y', linestyle='--')
plt.legend()
plt.ylabel('average score')
plt.xlabel('average score')
plt.savefig('../pic/like.png', dpi=400, bbox_inches='tight')
plt.show()
