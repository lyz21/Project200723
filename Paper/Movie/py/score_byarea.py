# encoding=utf-8
"""
@Time : 2020/7/26 12:49 
@Author : LiuYanZhe
@File : score_byarea.py 
@Software: PyCharm
@Description: 按喜好电影地区不同，分析评分
按照爱好的不同地区，计算每个地区的平均评分，使用线性拟合数据，表示变化趋势
需要先运行total_area.py获得csv文件，再读取获得的文件进行分析
输出为png文件
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit


def curve_fit_fun1(x, a, b):
    return a * x + b


def curve_fit_fun2(x, a, b, c):
    return a * (x ** 2) + b * x + c


data_cn = pd.read_csv('../data/country_area.csv')
data_red = pd.read_csv('../data/red_area.csv')
data_three = pd.read_csv('../data/three_area.csv')
data_earth = pd.read_csv('../data/earth_area.csv')
data_dark = pd.read_csv('../data/nezha_area.csv')
cn_list = {}
red_list = {}
th_list = {}
earth_list = {}
dark_list = {}
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in x:
    # 分别获取分数
    sc_cn = data_cn.iloc[list(data_cn['国产电影数量'] == i), 0].values
    sc_red = data_red.iloc[list(data_red['国产电影数量'] == i), 0].values
    sc_th = data_three.iloc[list(data_three['国产电影数量'] == i), 0].values
    sc_earth = data_earth.iloc[list(data_earth['国产电影数量'] == i), 0].values
    sc_dark = data_dark.iloc[list(data_dark['国产电影数量'] == i), 0].values
    # 计算平均分
    if len(sc_cn) == 0:
        mean_cn = 0
    else:
        mean_cn = np.mean(sc_cn)
        cn_list[i] = mean_cn
    if len(sc_red) == 0:
        mean_red = 0
    else:
        mean_red = np.mean(sc_red)
        red_list[i] = mean_red
    if len(sc_th) == 0:
        mean_th = 0
    else:
        mean_th = np.mean(sc_th)
        th_list[i] = mean_th
    if len(sc_earth) == 0:
        mean_th = 0
    else:
        mean_earth = np.mean(sc_earth)
        earth_list[i] = mean_earth
    if len(sc_dark) != 0:
        mean_dark = np.mean(sc_dark)
        dark_list[i] = mean_dark

# 绘图
ax = plt.subplot(1, 1, 1)
# 拟合方程
curve_fit_fun = curve_fit_fun1
x_t = list(cn_list.keys())
y_t = list(cn_list.values())
# ax.plot(list(range(1, len(cn_list) + 1)), cn_list, color='r', label='My People,My Country')
ax.scatter(x_t, y_t, color='b', alpha=0.6, label='My People,My Country')
a1, b1 = curve_fit(curve_fit_fun, x_t, y_t)[0]  # 线性拟合,返回值为[[参数值a,b],[概率]]
x1 = np.arange(min(x_t), max(x_t) + 1, 1)
y1 = a1 * x1 + b1
ax.plot(x1, y1, color='b', alpha=0.6)

x_t = list(red_list.keys())
y_t = list(red_list.values())
ax.scatter(x_t, y_t, color='g', alpha=0.8, label='Operation Red Sea')
a2, b2 = curve_fit(curve_fit_fun, x_t, y_t)[0]
x2 = np.arange(min(x_t), max(x_t) + 1, 1)
y2 = a2 * x2 + b2
ax.plot(x2, y2, color='g', alpha=0.8)

x_t = list(th_list.keys())
y_t = list(th_list.values())
ax.scatter(x_t, y_t, color='r', alpha=0.8, label='Three Billboards Outside')
a3, b3 = curve_fit(curve_fit_fun, x_t, y_t)[0]
x3 = np.arange(min(x_t), max(x_t) + 1, 1)
y3 = a3 * x3 + b3
ax.plot(x3, y3, color='r', alpha=0.8)

x_t = list(earth_list.keys())
y_t = list(earth_list.values())
ax.scatter(x_t, y_t, color='c', alpha=0.8, label='The Wandering Earth')
a4, b4 = curve_fit(curve_fit_fun, x_t, y_t)[0]
x4 = np.arange(min(x_t), max(x_t) + 1, 1)
y4 = a4 * x4 + b4
ax.plot(x4, y4, color='c', alpha=0.8)

x_t = list(dark_list.keys())
y_t = list(dark_list.values())
ax.scatter(x_t, y_t, color='y', alpha=0.8, label='Ne Zha')
a5, b5 = curve_fit(curve_fit_fun, x_t, y_t)[0]
x5 = np.arange(min(x_t), max(x_t) + 1, 1)
y5 = a5 * x5 + b5
ax.plot(x5, y5, color='y', alpha=0.8)
# 折线平滑
# window_length = 3  # 窗口长度，越大平滑越明显
# polyorder = 1  # 多项式拟合的阶数，越小平滑越明显
# ax.plot(list(range(1, len(cn_list) + 1)), savgol_filter(cn_list, window_length, polyorder), color='r', linestyle='--')
# ax.plot(list(range(1, len(red_list) + 1)), savgol_filter(red_list, window_length, polyorder), color='g',
#         linestyle='--')
# ax.plot(list(range(1, len(th_list) + 1)), savgol_filter(th_list, window_length, polyorder), color='y', linestyle='--')
plt.legend()
plt.ylabel('Average Score')
plt.xlabel('Attention to domestic films')
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8], [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1])
# plt.xlim([0, 9])
plt.savefig('../pic/like.png', dpi=400, bbox_inches='tight')
plt.show()
