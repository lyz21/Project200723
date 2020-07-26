# encoding=utf-8
"""
@Time : 2020/7/25 15:43 
@Author : LiuYanZhe
@File : testpic.py 
@Software: PyCharm
@Description: 
"""
import matplotlib.pyplot as plt

ax = plt.subplot(1, 1, 1)
ax.scatter([2, 1, 2], [1, 1, 2], s=[2, 2, 3], c=[1, 2, 2], lw=10)
plt.show()
