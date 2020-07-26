"""
Apriori算法   python实现
2019.09.24 19:13
lyz

数据来源于《数据挖掘方法》P33    在此数据中，若使用support直接计算可信度，会丧失精度，2->3结果为0.7999...,使用计数相除可保持精度，结果为0.8
support(X) = count(X)/D
support(X => Y) = count(X,Y)/D
confidence(X => Y) = support(X => Y)/support(X) = count(X,Y)/count(X)
"""
from numpy import *
import logging
from Paper.Movie.util import wordUtil


'''日志设置'''
logging.basicConfig(filename='test2_logging.txt', filemode='w', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
# 禁用日志
logging.disable()
# 最低支持度和最低置信度
# MINSUP = 0.5
# MINCONF = 0.9
MINSUP = 0.1
MINCONF = 0.1

# 删去的项，剪枝用
LISTDEL = []
# 事务个数
T = 0
# 1-项集
LIST1 = []
# 保存各个项支持度计数(两个列表下标一一对应),因为KEY值很可能为list，所以不能用字典类型
LISTSUPKEY = []
LISTSUPVALUE = []
# 保存各项计数
LISTCOUNTKEY = []
LISTCOUNTVAL = []

# 存储1-1对应关系，画图用
LISTCORR = []
SETNODE = set()
# 存储图像设置
PICNAME = '../pic/apriori_title1_0414.png'
# TITLE = 'January 1 to March 28'
# TITLE = 'January 1 to January 25'
# TITLE = 'January 26 to February 09'
# TITLE = 'February 10 to March 28'
TITLE = '(a) 1月1日-1月25日'


# TITLE = '(b) 1月26日-2月9日'
# TITLE = '(c) 2月10日-3月28日'


# 载入数据
def loadDate():
    data = wordUtil.get_words_list2('../data/countryComment.csv')
    # data = loadData.loadData()
    # data = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'], ['I2', 'I3'],
    #         ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]
    # data = [['1', '2', '5'], ['2', '4'], ['2', '3'], ['1', '2', '4'], ['1', '3'], ['2', '3'],
    #         ['1', '3'], ['1', '2', '3', '5'], ['1', '2', '3']]
    # data = [['1', '2', '3'], ['4', '1'], ['4', '5'], ['1', '2', '4'], ['1', '2', '6', '4', '3'], ['2', '6', '3'],
    #         ['2', '3', '6']]

    print('原数据项数：', len(data))
    tempData = []
    for items in data:
        items = sorted(items)
        tempData.append(items)
    print('loadData方法输出数据：', tempData)
    return tempData


# 获得事务个数
def getTransNum(dataSet):
    global T
    T = len(dataSet)


# 找出1-项候选集
def C1(dataSet):
    logging.debug('-----------------------C1------------')
    global LISTSUPKEY
    global LISTSUPVALUE
    # 使用字典统计个数
    tempdic = {}
    # 声明使用的全局变量
    global LIST1, LISTDEL, LISTCOUNTKEY, LISTCOUNTVAL
    # 遍历出里面的每个元素，并计数
    for iterw in dataSet:
        for itern in iterw:
            tempdic.setdefault(itern, 0)
            tempdic[itern] = tempdic[itern] + 1
    logging.debug('tempdic=' + str(tempdic))

    # 筛选满足最低支持度的项集，保存到list中
    for k, v in tempdic.items():
        logging.debug('T:' + str(T))
        logging.debug(str(k) + ':' + str(v) + ';support=' + str(v / T))
        # 计数存入变量
        temp = []
        temp.append(k)
        LISTCOUNTKEY.append(temp)
        LISTCOUNTVAL.append(v)
        if ((v / T) > MINSUP) or ((v / T) == MINSUP):
            LIST1.append(k)
            temp = []
            temp.append(k)
            LISTSUPKEY.append(temp)
            LISTSUPVALUE.append(v / T)
        else:
            LISTDEL.append(k)
    LIST1 = sorted(LIST1)
    print('1-项频繁集：', str(LIST1))
    logging.debug('-------------------')
    return LIST1


# 连接。生成k+1项候选集,Ck为上一步生成的k-项频繁集
def createK(CK):
    logging.debug('------------------createK---------')
    logging.debug('连接传入CK:' + str(CK))
    TempCK = []
    # 连接组合
    for itme1 in CK:
        for i in LIST1:
            # 如果Ck==LIST1，说明CK内部是str不是[]
            if CK == LIST1:
                # 由1项生成2项时，会有（1，1情况出现）
                if i == itme1:
                    continue
                tempList = []
                tempList.append(itme1)
                tempList.append(i)
                tempList.sort()
                TempCK.append(tempList)
            else:
                if i not in itme1:
                    tempList = itme1.copy()
                    tempList.append(i)
                    tempList.sort()
                    # logging.debug('tempList:'+str(tempList))
                    TempCK.append(tempList)
    logging.debug('TempCK:' + str(TempCK))
    # 去重
    TempCk2 = []
    for item in TempCK:
        if item not in TempCk2:
            TempCk2.append(item)
    logging.debug('TempCK2:' + str(TempCk2))
    logging.debug('----------------------')
    return TempCk2


# 剪枝。(pruning:剪枝)
def pruning(CK):
    logging.debug('----------------------------pruning----')
    logging.debug('剪枝传入CK:' + str(CK))
    TempList = []
    logging.debug('LISTDEL:' + str(LISTDEL))
    for item2 in CK:
        if len(LISTDEL) == 0:
            TempList.append(item2)
        else:
            for item1 in LISTDEL:
                if item1 not in item2:
                    TempList.append(item2)
    # 去重（此处可优化，本来剪枝不需要去重，筛选即可，但是此剪枝方法会造成重复，因此需去重）
    Temp = []
    for item in TempList:
        if item not in Temp:
            Temp.append(item)
    logging.debug('Temp:' + str(Temp))
    logging.debug('----------------------------')
    return Temp


# 剔除。得到k-项频繁集
def getFrequentK(CK, dataList):
    logging.debug('---------------------getFrequentK-----')
    logging.debug('剔除传入CK：' + str(CK))
    global LISTSUPKEY
    global LISTSUPVALUE
    # 统计项计数
    global LISTCOUNTVAL, LISTCOUNTKEY
    TempList1 = []
    j = 0
    # 查找第一个候选项支持度计数，结果保存到list中，下标与CK下标对应
    for f1 in CK:
        logging.debug('f1:' + str(f1))
        num = 0
        for d in dataList:
            logging.debug('d:' + str(d))
            flag = 1
            for f2 in f1:
                logging.debug('f2:' + str(f2))
                logging.debug('f2 not in d:' + str(f2 not in d))
                if f2 not in d:
                    flag = 0
                logging.debug('flag:' + str(flag))
            if flag == 1:
                num += 1
                logging.debug('num:' + str(num))
        TempList1.append(num)
        logging.debug('TempList1---:' + str(TempList1))
        j += 1
        logging.debug('TempList1：' + str(TempList1))
    # 筛选出满足最低支持度的频繁集
    TempList2 = []
    print('K项频繁集：')
    for i in range(len(TempList1)):
        if ((TempList1[i] / T) > MINSUP) or ((TempList1[i] / T) == MINSUP):
            TempList2.append(CK[i])
            LISTSUPKEY.append(CK[i])
            LISTSUPVALUE.append(TempList1[i] / T)
            # 计数存入全局变量
            LISTCOUNTKEY.append(CK[i])
            LISTCOUNTVAL.append(TempList1[i])
    print('TempList2:', str(TempList2))
    logging.debug('------------------------------')
    return TempList2


# 生成list的所有子集，生成关联规则用（使用二进制法）,除去空集和集合本身
def powerSetsBinary(frequentK):
    logging.debug('----------------powerSetsBinary------')
    templist = []
    for items in frequentK:
        templist2 = []
        N = len(items)
        for i in range(2 ** N):  # 子集的个数,2的n次方个
            combo = []
            for j in range(N):  # 用来判断二进制数的下标为j的位置的数是否为1，通过下面移位运算实现
                if (i >> j) % 2:  # 将i的二进制数向右移动j位后的十进制数
                    combo.append(items[j])
            if (combo == items) or len(combo) == 0:
                continue
            templist2.append(combo)
        templist.append(templist2)
    logging.debug('-----------------------------')
    return templist


# 判断两个列表之间元素是否有重合（生成关联规则用）
def boolIn(list1, list2):
    logging.debug('---------------------boolIn-----')
    flag = 0
    for item in list1:
        if item in list2:
            flag = 1
    logging.debug('--------------')
    if flag == 0:
        return False
    else:
        return True


# 计算关联规则的可信度和支持度 conf(X=>Y)=support(x,y)/support(x)
def makeConf(list1, list2):
    logging.debug('-----------makeConf()')
    temp = list1 + list2
    logging.debug('temp=' + str(temp))
    temp = sorted(temp)
    logging.debug('sort(temp)=' + str(temp))
    '''
    # 使用support计算可信度
    xy = LISTSUPKEY.index(temp)
    xy_v = LISTSUPVALUE[xy]
    logging.debug('sup(' + str(temp) + ')=' + str(xy_v))
    x = LISTSUPKEY.index(list1)
    x_v = LISTSUPVALUE[x]
    logging.debug('sup(' + str(list1) + ')=' + str(x_v))
    conf = xy_v / x_v
    print('support计算的可信度：',conf)
    '''
    # 使用计数计算可信度
    xy = LISTCOUNTKEY.index(temp)
    xy_v = LISTCOUNTVAL[xy]
    x = LISTCOUNTKEY.index(list1)
    x_v = LISTCOUNTVAL[x]
    conf = xy_v / x_v
    # print('count计算的可信度：',conf)
    # print(str(temp), ':', xy_v)
    # print(('规则：' + str(list1) + '--->' + str(list2)))
    support = xy_v / T
    templist = [conf, support]
    logging.debug('conf:' + str(conf))
    logging.debug('规则：' + str(list1) + '--->' + str(list2))
    logging.debug('------------')
    return templist


# 生成关联规则
def createRule(sonList):
    logging.debug('---------------------createRule------')
    for items1 in sonList:

        for items2a in items1:
            for items2b in items1:
                # 两个列表之间元素有重合，跳出此次循环
                if boolIn(items2a, items2b):
                    continue
                # 组合规则
                tempList = makeConf(items2a, items2b)
                if tempList[0] > MINCONF or tempList[0] == MINCONF:
                    logging.debug('规则：' + str(items2a) + '--->' + str(items2b))
                    # if内的语句，绘图用的数据
                    if len(items2a) == 1 and len(items2b) == 1:
                        LISTCORR.append([items2a[0], items2b[0], tempList[1]])
                        SETNODE.add(items2a[0])
                        SETNODE.add(items2b[0])
                    print('规则：', str(items2a), '--->', str(items2b), '   可信度为：', str(tempList[0]), '    支持度为：',
                          str(tempList[1]))
                    # print('规则：', NAME[str(items2a)], '--->', NAME[str(items2b)], '   可信度为：', str(conf))


# 形成Apriori方法
def Apriori():
    # 获取原始数据
    dataList = loadDate()
    # 获取项数
    getTransNum(dataList)
    # 获取1-项频繁集
    list = C1(dataList)
    tempList = []
    while True:
        # 获取k-项候选集
        list = createK(list)
        # 剪枝
        list = pruning(list)
        # 剔除
        list = getFrequentK(list, dataList)
        if len(list) == 0:
            break
        tempList = list

    # 获得频繁集的子集
    sonList = powerSetsBinary(tempList)
    # 形成并输出规则
    createRule(sonList)

    # print('sonList:', str(sonList))
    print('----------------')
    print('支持度统计:')
    print('LISTSUPVALUE:', str(LISTSUPVALUE))
    print('LISTSUPKEY:', str(LISTSUPKEY))
    print('各项计数统计：')
    print(str(LISTCOUNTKEY))
    print(str(LISTCOUNTVAL))





if __name__ == '__main__':
    # 调用Apriori方法
    Apriori()
    print(LISTCORR)
    print(SETNODE)
    # # LISTCORR =
    # # SETNODE = {'工作', '群众', '会议', '疫情', '做好', '责任', '抓好', '全面', '保障', '防控'}
    # # DrawUtil.Draw(LISTCORR, SETNODE, '../pic/apriori3.png', title='February 17 to March 28')

    # Draw(LISTCORR, SETNODE, PICNAME, title=TITLE)
