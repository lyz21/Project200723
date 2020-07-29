# encoding=utf-8
"""
Name:         doubanComment
Description:  爬取豆瓣电影详细评论（包括评论人信息）
运行：
需更改：
1、修改URL参数，设定要获取的电影路径
2、WORKBOOKNAME，设定要保存的文件路径
一般不需更改
3、ENTRYNUM设定每页爬取的条数，豆瓣默认20条
4、STARTSUB为起始下标，默认从0开始，需要接上以前的话，可更改
5、T为爬取间隔时间，防止封ip
6、如果使用proxies代理池，需要先使用download_ip或download_ip2获得并存储ip代理池文件
Author:       LiuYanZhe
Date:         2019/10/28
"""
# 下载页面
import requests
# 分析页面（清洗数据）
import bs4
# 处理表格
import openpyxl
# 目录控制
import os
# 日志模块
import logging
# 控制运行时间
import time
# 正则表达式模块
import re
import pandas as pd
import random

'''日志设置'''
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志
logging.disable()
'''全局变量'''
# 工作目录
# WORKSPACE = 'E:/data_lyz'
# 每页条数
ENTRYNUM = 20
# 起始下标
STARTSUB = 220
# 下载链接
# URL = 'https://movie.douban.com/subject/26861685/comments?start='     # 红海行动
URL = 'https://movie.douban.com/subject/32659890/comments?start='  # 我和我的祖国
# URL = 'https://movie.douban.com/subject/26761416/comments?start='  # 至暗时刻
# URL = 'https://movie.douban.com/subject/26611804/comments?start='  # 三块广告牌
# URL = 'https://movie.douban.com/subject/26266893/comments?start='  # 流浪地球
# URL = 'https://movie.douban.com/subject/26794435/comments?start='  # 哪吒
# 每次爬取的间隔时间
T = 2
# 保存的文件名
WORKBOOKNAME = '../data/豆瓣我和我的祖国影评2.xlsx'
# WORKBOOKNAME = '../data/流浪地球豆瓣影评2.xlsx'
# WORKBOOKNAME = '../data/哪吒豆瓣影评.xlsx'
# WORKBOOKNAME = '../data/三块广告牌豆瓣影评2.xlsx'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}  # 请求头
'''excel相关'''


# 设置工作目录
# os.chdir(WORKSPACE)


# 去除字符串空格、换行方法
def delspace(string):
    # 去除换行
    string = string.replace('\n', '')
    # 去除空格
    string = string.replace(' ', '')
    # 去除两边空格
    string = string.strip()
    return string


proxies_list = pd.read_csv('../data/ip.csv').values


# 获取网页方法,返回soup对象进行数据清洗
def getrequest(url):
    # 为避免ip被封，限制每分钟爬取次数
    time.sleep(T)
    # 获取网页response对象
    sub = random.randint(0, len(proxies_list))
    proxies = proxies_list[sub][0]
    proxies = eval(proxies)
    # proxies = {'https': '159.8.114.37:80'}
    print('代理IP地址：', proxies)
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        # 乱码处理
        response.encoding = 'utf-8'
        # 监控网页状态
        try:
            # response.encoding = response.apparent_encoding
            print(response.status_code)
            response.raise_for_status()
            # 获取soup对象，BeautuifulSoup清洗数据
            soup = bs4.BeautifulSoup(response.text)
            return soup
        except requests.exceptions.HTTPError:
            print(response.text)
            soup = '无'
            print('获取网页出错！')
            time.sleep(T)
            return soup
    except requests.ConnectionError:
        print('ip连接错误')
        getrequest(url)
    # return soup


# 获取链接为url的用户信息
def getuser_information(url):
    logging.debug('获取用户数据' + url)
    # 为避免ip被封，限制每分钟爬取次数
    time.sleep(T)
    # 通过url获取用户页面，并返回soup对象进行数据清洗
    soup = getrequest(url)
    if soup == '无':
        return '无', ['无']
    '''找位置 直接用bs4找不到，结合正则表达式使用'''
    # 获取标签内容
    infohtml = soup.select('.user-info')
    # 将bs4数据类型转为string类型
    if len(infohtml) > 0:
        str1 = str(infohtml[0])
        # 设定正则表达式匹配模式,找到位置
        comp = re.compile(r'/">.*</a>')
        infotemp = comp.search(str1)
        try:
            pos = infotemp.group().replace(r'/">', '').replace(r'</a>', '')
        except AttributeError:
            pos = '无'
            print('获取用户信息出错！')
            time.sleep(T)
    else:
        pos = '无'
    '''找想看和看过的电影链接'''
    likemovie = soup.select('div[id="movie"]>div[class="obssin"]>ul>.aob>a')
    return pos, likemovie


# 获取电影名链接为url的信息（主要找 地区）
def getmovie_information(url):
    logging.debug('获取电影信息:' + url)
    # 为避免ip被封，限制每分钟爬取次数
    time.sleep(T)
    # 通过url获取用户页面，并返回soup对象进行数据清洗
    soup = getrequest(url)
    if soup == '无':
        return '无'
    # 获取整个div下的html
    html_list = soup.select('div[id="info"]')
    # 转换为str
    if len(html_list[0]) > 0:
        html_str = str(html_list[0])
        # 设定正则表达式找出含地区的标签
        comp = re.compile(r'地区:</span>.*<br/>')
        position_html = comp.search(html_str)
        # 去掉标签内容，找出地区并去空格
        position = position_html.group().replace('地区:</span>', '').replace('<br/>', '').replace(' ', '')
    else:
        position = '无'

    return position


# 通过用户url获取观看标签     有反爬取，无法进入页面
# def getlabel(url):
#     # 重定向页面
#     url=url+'collect'
#     # 获取soup
#     soup=getrequest(url)
#     print(soup)
# getlabel('https://www.douban.com/people/155986723/')


# 创建workbook对象
workbook = openpyxl.Workbook()
# 获取当前sheet对象（表格）
# sheet = workbook.get_active_sheet()
sheet = workbook.active
# 设行名
sheet['A1'] = '评分'
sheet['A2'] = '评论日期'
sheet['A3'] = '评论内容'
sheet['A4'] = '认同人数'
sheet['A5'] = '评论人所在城市'
sheet['A6'] = '评论人ID'
sheet['A7'] = '评论人喜欢的电影名'
sheet['A17'] = '喜欢的电影地区'
for n in range(20):
    '''读取网页'''
    # 拼接url
    TURL = URL + str(STARTSUB)
    # 通过链接获取网页并转换为soup对象，得到soup对象，使用BeautuifulSoup进行数据清洗
    print('TURL:', TURL)
    soup = getrequest(TURL)
    ''' 评论内容（下面两种方法）'''
    # 找到class=short的标签数据
    if soup == '无':
        print('URL出错')
        continue
    elems_comment = soup.select('.short')
    # 找到span标签下class=‘short’的数据
    # elems_comment=soup.select('span[class="short"]')
    ''' 评分 含有title属性的span标签'''
    elems_score = soup.select('span[title]')  # 得到本标签内容
    '''评论人链接，span标签下的a标签'''
    elems_user_link = soup.select('span>a')
    user_link_list = []
    for i in range(len(elems_user_link)):
        temp = elems_user_link[i].get('href')
        if temp == 'javascript:;':
            continue
        user_link_list.append(temp)
    '''点赞数'''
    elems_vote = soup.select('.votes')
    print('本页起始下标：', str(STARTSUB))
    # 读取本页的评论信息
    k = 0  # 记录score下标
    flag = 0
    for i in range(len(elems_comment)):
        print('第 ', str(i), ' 个评论')
        # 列号
        c = n * 20 + i + 2
        # 按列存储
        column = openpyxl.utils.get_column_letter(c)
        # 获得score
        if flag == 0:  # 正常情况
            temp_score = elems_score[2 * k].get('class')  # 得到['allstar40', 'rating']
            score = temp_score[0].replace('allstar', '')  # 得到40
            if score == 'comment-time':  # 若缺少一个评分，更改本次，同时更换方式
                # 评论日期
                temp_data = elems_score[(2 * k)].getText()
                flag = 1
            else:  # 正常
                # 评论日期
                temp_data = elems_score[(2 * k + 1)].getText()
        else:
            temp_score = elems_score[2 * k - 1].get('class')  # 得到['allstar40', 'rating']
            score = temp_score[0].replace('allstar', '')  # 得到40
            if score == 'comment-time':  # 若缺少一个评分
                # 评论日期
                k = k - 1
                temp_data = elems_score[(2 * k + 1)].getText()
                flag = 0
            else:  # 正常
                # 评论日期
                temp_data = elems_score[(2 * k)].getText()
        # 去换行和空格
        data = delspace(temp_data)
        print('评分：', score)
        sheet[column + '1'] = score
        print('评论日期：', data)
        sheet[column + '2'] = data
        # 评论内容
        content = elems_comment[i].getText()
        print('评论内容：', content)
        sheet[column + '3'] = content
        # 赞同人数
        vote = elems_vote[i].getText()
        print('认同人数：', vote)
        sheet[column + '4'] = vote
        # 评论人链接
        user_link = user_link_list[i]
        # print('评论人链接：',user_link )
        print('评论人链接：', user_link)
        # 评论人信息
        position, likemovie_list = getuser_information(user_link_list[i])
        print('评论人位置：', position)
        sheet[column + '5'] = position
        # 获取评论人ID
        try:
            comp = re.compile(r'people/.*/')
            user_id = comp.search(user_link).group().replace('people', '').replace('/', '')
            sheet[column + '6'] = user_id
        except:
            print('获取用户ID失败')
        # 评论人喜欢的电影名
        for j in range(len(likemovie_list)):
            # 评分
            movie_name = likemovie_list[j].get('title')
            movie_name = delspace(movie_name)  # 去换行和空格
            print('评论人喜欢的电影名：', movie_name)
            sub = j + 7
            sheet[column + str(sub)] = movie_name
            # 喜欢的电影链接
            movie_link = likemovie_list[j].get('href')
            # print('喜欢的电影链接：', movie_link)
            # 根据链接找到电影所属地区
            movie_position = getmovie_information(movie_link)
            print('喜欢的电影地区：', movie_position)
            sub = j + 7 + 10
            sheet[column + str(sub)] = movie_position
            # 设置表名,标明为页号
            sheet.title = str('评论')
            # 保存文件
            workbook.save(WORKBOOKNAME)
            print('第', str(n), '页已存储')
        k += 1
    # 更新起始下标
    STARTSUB = STARTSUB + 20

# 存储评论相关类
# class Comment:
#     def __init__(self):
#         print('评分：', score)
#         print('评论日期：', data)
#         print('评论内容：',elems_comment[i].getText())
#         print('评论人：',elems_user_link)
#         # print('评论人：',elems_user_link[2*i].get('href'))
#         print('认同人数：',elems_vote[i].getText())
#         self.score='0'
#         self.
