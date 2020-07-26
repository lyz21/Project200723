# encoding=utf-8
"""
@Time : 2020/7/26 15:33 
@Author : LiuYanZhe
@File : net.py 
@Software: PyCharm
@Description: 网络图
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# 绘制网络图方法，csv为pd类型的关联矩阵，存储格式为df1[['word1']['word2']]，pic_path为保存路径
def draw(csv_path, pic_path):
    # 获取关联矩阵
    matrix = pd.read_csv(csv_path)
    data_matrix = matrix.iloc[:, 1:]
    # 获取索引值
    word_list = matrix.iloc[:, 0]
    data_matrix.index = word_list
    # true_word_set = set()
    # 存储映射的列表
    list_mapping = []
    # 维度转换
    for i in range(len(word_list)):
        for j in range(len(word_list)):
            if data_matrix[word_list[i]][word_list[j]] != 0:
                # if data_matrix[word_list[i]][word_list[j]] > 1:  # 筛选连接超过1的
                #     true_word_set.add(word_list[i])
                #     true_word_set.add(word_list[j])
                list_mapping.append([word_list[i], word_list[j], data_matrix[word_list[i]][word_list[j]]])
    print('list_mapping:', list_mapping)
    print('word_list:', word_list)
    # 绘图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题，目前只知道黑体可行
    G = nx.Graph()
    G.add_nodes_from(word_list)  # 设置节点
    G.add_weighted_edges_from(list_mapping)  # 设置边
    # pos = nx.circular_layout(G)   #节点在一个圆环上均匀分布
    # pos = nx.shell_layout(G)  # 节点在同心圆上分布
    # pos = nx.random_layout(G)  # 节点随机分布
    pos = nx.spring_layout(G)  # 用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
    # pos = nx.spectral_layout(G)  # 根据图的拉普拉斯特征向量排列节点
    # 绘制网络图
    # nx.draw(G, pos, with_labels=True, width=0.5, node_size=6, alpha=0.8, font_weight='bold', font_size=7,
    #         font_color='r')
    # 绘制网络图-边宽为权重
    # nx.draw(G, pos, with_labels=True, width=[float(v['weight'] / 4) for (r, c, v) in G.edges(data=True)], node_size=6,
    #         alpha=0.8, font_weight='bold', font_size=7,
    #         font_color='r')
    nx.draw(G, pos, with_labels=True, width=[float(v['weight'] / 1.0) for (r, c, v) in G.edges(data=True)],
            node_size=800,
            alpha=0.8, font_weight='bold', font_size=11,
            font_color='w', node_color='k', edge_color='k') #
    plt.savefig(pic_path, dpi=600, bbox_inches='tight', figsize=(4000, 2250))
    plt.show()


apriori = pd.read_csv('../data/apriori.csv')
apriori = apriori.fillna(-1)
apriori = apriori.values
print(apriori)
# 词汇列表
word_set = set()
for item in apriori:
    for word in item:
        if word != -1:
            word_set.add(word)
print(word_set)
# 构建连接矩阵
keyword_matrix = pd.DataFrame(np.zeros((len(word_set), len(word_set))), columns=word_set, index=word_set)
print(keyword_matrix)
# 为连接矩阵赋值
for item in apriori:
    for i in range(len(item) - 1):
        if item[i] == -1:
            continue
        for j in range(i + 1, len(item)):
            if item[j] == -1:
                continue
            print(keyword_matrix[item[i]][item[j]])
            keyword_matrix[item[i]][item[j]] += 1
print(keyword_matrix)

path = '../data/apriori_matrix.csv'
keyword_matrix.to_csv(path)
draw(path, '../pic/apriori_net.png')
