# encoding=utf-8
"""
@Time : 2020/7/26 11:25 
@Author : LiuYanZhe
@File : total_area.py 
@Software: PyCharm
@Description: 统计每个用户关注的地区
"""
import pandas as pd
import numpy as np


# 统计每个用户关注国产电影的比例
def total_area(path, save_path):
    data = pd.read_excel(path)
    # 填充缺失值
    data = data.fillna(-1)
    # 提取评分
    score = data.iloc[:, 0].copy()
    # 提取国家信息
    country = data.iloc[:, 16:25].values
    # 统计中国的个数
    num_list = []
    for item in country:
        num_list.append(np.sum(item == '中国大陆'))
    cn_pd = pd.DataFrame(score)
    cn_pd['国产电影数量'] = num_list
    cn_pd = cn_pd.iloc[list(cn_pd['评分'] != 'comment-time'), :]
    cn_pd.to_csv(save_path, index=False)


if __name__ == '__main__':
    # total_area('../data/我和我的祖国豆瓣影评.xlsx', '../data/country_area.csv')
    # total_area('../data/三块广告牌豆瓣影评T.xlsx', '../data/three_area.csv')
    total_area('../data/红海行动豆瓣影评.xlsx', '../data/red_area.csv')
