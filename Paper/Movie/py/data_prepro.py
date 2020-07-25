# encoding=utf-8
"""
@Time : 2020/7/24 15:56 
@Author : LiuYanZhe
@File : data_prepro.py 
@Software: PyCharm
@Description: 数据预处理,将excel转化为csv格式，并把数据做部分处理
"""
import pandas as pd

# 将excel数据读取为pd类型
country_dou = pd.read_excel('../data/我和我的祖国豆瓣影评.xlsx')
country_dou = country_dou.iloc[:, :4]
print(country_dou)

country_time = pd.read_excel('../data/我和我的祖国时光网影评.xlsx')
country_time = country_time.loc[:, ['评分', '评论时间', '评论']]
country_time['认同人数'] = 0
country_time.columns = ['评分', '评论日期', '评论内容', '认同人数']
country_time['评分'] = country_time['评分'] * 5
country_time.iloc[list(country_time['评分'] <= 10), 0] = 10
country_time.iloc[list((country_time['评分'] > 10) & (country_time['评分'] <= 20)), 0] = 20
country_time.iloc[list((country_time['评分'] > 20) & (country_time['评分'] <= 30)), 0] = 30
country_time.iloc[list((country_time['评分'] > 30) & (country_time['评分'] <= 40)), 0] = 40
country_time.iloc[list(country_time['评分'] > 40), 0] = 50
print(country_time)
country = pd.concat([country_dou, country_time], axis=0)
country = country.reset_index(drop=True)
print(country)
time = country['评论日期'].str.split(' ', expand=True).iloc[:, 0]
print(time)
country['评论日期'] = time
country.to_csv('../data/countryComment.csv', index=False)
