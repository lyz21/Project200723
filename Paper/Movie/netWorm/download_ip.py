# encoding=utf-8
"""
@Time : 2020/7/27 19:33 
@Author : LiuYanZhe
@File : download_ip.py 
@Software: PyCharm
@Description: 从https://www.kuaidaili.com/下载代理IP
"""
# 下载页面
import requests
# 分析页面（清洗数据）
import bs4
import pandas as pd
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}  # 请求头
# 提取存入list
ip_list = []
for page in range(0, 100):
    # 暂停
    time.sleep(2)
    IPurl = 'https://www.kuaidaili.com/free/inha/%s' % page
    rIP = requests.get(IPurl, headers=headers)
    IPContent = rIP.text
    # 找标签
    soup = bs4.BeautifulSoup(IPContent)
    ips = soup.select('td[data-title="IP"]')
    ports = soup.select('td[data-title="PORT"]')
    types = soup.select('td[data-title="类型"]')
    for i in range(len(ips)):
        ip_path = ips[i].getText()
        ip_port = ports[i].getText()
        ip_type = types[i].getText()
        if ip_type == 'HTTP':
            ip_type = 'http'
        ip = ip_path + ':' + ip_port
        ip_dic = {}
        ip_dic[ip_type] = ip
        ip_list.append(ip_dic)
    # 存储
    ip_ser = pd.Series(ip_list)
    ip_ser.to_csv('../data/ip_http.csv', index=False)
    print('../data/ip_http.csv文件已保存')
