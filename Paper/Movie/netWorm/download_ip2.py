# encoding=utf-8
"""
@Time : 2020/7/28 15:23 
@Author : LiuYanZhe
@File : download_ip2.py 
@Software: PyCharm
@Description: 从http://www.ip3366.net/下载代理IP,主要获取https的ip
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
for page in range(100):
    # 暂停
    time.sleep(2)
    IPurl = 'http://www.ip3366.net/?stype=1&page=%s' % page
    rIP = requests.get(IPurl, headers=headers)
    IPContent = rIP.text
    # 找标签
    soup = bs4.BeautifulSoup(IPContent)
    td_list = soup.select('tr>td')
    for i in range(10):
        ip_path = td_list[i * 8].getText()
        ip_port = td_list[i * 8 + 1].getText()
        ip_type = td_list[i * 8 + 3].getText()
        # 筛选只要https类型的ip
        if ip_type == 'HTTP':
            continue
        ip_type = 'https'
        ip = ip_path + ':' + ip_port
        ip_dic = {}
        ip_dic[ip_type] = ip
        ip_list.append(ip_dic)
    # 存储
    ip_ser = pd.Series(ip_list)
    print(ip_ser)
    ip_ser.to_csv('../data/ip_https.csv', index=False)
    print('../data/ip_https.csv文件已保存')
print(ip_list)
