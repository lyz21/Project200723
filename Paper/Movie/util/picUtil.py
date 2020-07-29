# encoding=utf-8
"""
@Time : 2020/7/24 22:31 
@Author : LiuYanZhe
@File : picUtil.py 
@Software: PyCharm
@Description: 绘图工具类
"""
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt


# 绘制词云图，输入为一维数组
def draw_word_cloud(words_dic):
    font_path = 'C://Windows//Fonts//STXINGKA.TTF'
    # stop_words = pd.read_csv('../data/hit_stopwords.csv')
    stop_words = ['电影', '故事', '看', '人', '没有']
    # print(stop_words)
    for word in stop_words:
        words_dic.pop(word)
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=font_path,  # 这个路径是pc中的字体路径
        # 设置背景色
        # background_color='#383838',
        background_color='white',
        # color_func=random_color_func,
        # mode='RGBA',
        # colormap='Blues',  # 风格  Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r
        # 词云形状
        # mask=color_mask,
        # 允许最大词汇
        max_words=2000,
        # 缩放(可以控制字体的清晰度)
        scale=8,
        # 最大号字体
        max_font_size=170, width=1000, height=600,
        # stopwords=stopwords,
    )
    word_cloud = cloud.generate_from_frequencies(words_dic)
    word_cloud.to_file("../pic/wordCloud.png")  # 保存图片
