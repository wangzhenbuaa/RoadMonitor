import numpy as np
import pandas as pd
import math
import glob

path1 = './ACCL/new1/*.csv'
path2 = './GPS5/*.csv'
strTemp = path1[:-10]
dataList = glob.glob(path1)
gpsList = glob.glob(path2)
numFile = len(dataList)
print('to solve %d files' % numFile)
logFile = open('log.txt', 'a')
gamaFile = open('gama.txt', 'a')
gama = []  # 保存所有gama角, gama角为汽车行驶方向与当前坐标系Y轴夹角


def timeToRowNum(time):
    return int(time * 100)


# 将汽车行驶方向与X轴夹角转化为与Y轴夹角
# atan2(y,x)所求为汽车行驶方向与X轴夹角
def angelTrans(angel):
    angel = 90 - angel
    if angel > 180:
        angel -= 360
    return angel


# 第一阶段，计算gama
winSize = 6000  # large window 6000行 - 2min
smallWinSize = 300  # small window 300行 - 6s
slidingStep = 100  # 小窗口滑动步长 - 2s
for fileIndex in range(numFile):
    logFile.write('--------------------------' + '文件' + str(fileIndex + 1) + '---------------------------------' + '\n')
    gamaFile.write(
        '--------------------------' + '文件' + str(fileIndex + 1) + '---------------------------------' + '\n')
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    gpsData = pd.read_csv(gpsList[fileIndex], encoding='utf-8')
    print(data.shape)
    gamaTemp = []
    x1 = data['x1']
    y1 = data['y1']
    z1 = data['z1']
    rLevel = [math.sqrt(x1[i] * x1[i] + y1[i] * y1[i]) for i in range(len(x1))]
    t = data['time']
    v = gpsData['GPS (2D speed) [m/s]']
    low, high = 0, 0  # 大窗口边界
    winIndex = 0
    while low < len(x1):
        winIndex += 1
        high = min(low + winSize, len(x1))
        deltaZ, deltaV = [], []
        stRow, edRow = [], []
        left, right = low, low  # 小窗口边界
        # 获取deltaZ, deltaV，stRow, edRow
        while right + smallWinSize / 2 < high:
            right = min(left + smallWinSize, high)
            # 处理每个文件的最后一个窗口
            #4-2 14:57更改，未执行过
            if right == len(x1):
                right -= 1
            # 找到小窗口里最大z与最小z的差值
            deltaZ.append(max(z1[left:right]) - min(z1[left:right]))
            row1, row2 = timeToRowNum(t[left]), timeToRowNum(t[right])
            # print(left)
            deltaV.append(max(v[row1:row2]) - min(v[row1:row2]))
            stRow.append(left)
            edRow.append(right)
            left += slidingStep
        # 寻找最有可能为breaking or accelerating event的小窗口-----
        breakingIndex = -1  # 最有可能为刹车的窗口
        ans = [(deltaV[i] - deltaZ[i]) for i in range(len(deltaV))]
        for i in range(len(deltaV)):
            st, ed = stRow[i], edRow[i]
            # -----------------修复停车时，相机速度漂移bug----------------
            # ------------------此bug没法完全修复，还得人为参考视频验证---------
            # --------速度漂移有个特点，先加速再减速----------------------
            p1, p2 = timeToRowNum(t[st]), timeToRowNum(t[ed])
            pStep = int((p2 - p1) / 3)
            v1, v2, v3 = np.mean(v[p1:p1 + pStep]), np.mean(v[p1 + pStep:p1 + pStep * 2]), np.mean(v[p1 + pStep * 2:p2])
            if v2 > v1 and v2 > v3:
                continue
            # -----------------修复停车时，相机速度漂移bug----------------
            # ----判断为breaking窗口的阈值-------
            if deltaZ[i] < 1.5 and deltaV[i] > 5 and ans[i] > 4:  # 此处阈值应参考窗口大小修改
                if breakingIndex == -1:
                    breakingIndex = i
                elif ans[i] > ans[breakingIndex]:
                    breakingIndex = i

        # 记录一下日志从而验证
        logFile.write('第 ' + str(winIndex) + ' 个大窗口:' + '\n')
        if breakingIndex == -1:  # 没有找到breaking窗口
            logFile.write('没有找到breaking Or accelerating event' + '\n')
            gamaTemp.append('none')
        else:
            # ---------------在最有可能为刹车的窗口里找到水平加速度最大的5个点，从而求出gama
            # breaking or accelerating 窗口里水平加速度最大的5个点
            a, b = stRow[breakingIndex], edRow[breakingIndex]  # 找到breaking窗口的左右边界
            temp = np.argsort(rLevel[a:b]) + a  # 从小到大排序
            breakingIndex2 = temp[-5:]
            xTemp, yTemp = np.mean(x1[breakingIndex2]), np.mean(y1[breakingIndex2])
            gamaTemp_ = math.atan2(yTemp, xTemp)
            # 判断窗口为加速窗口还是减速窗口，若为减速窗口，则转换gamaTemp_值
            p1, p3 = timeToRowNum(t[a]), timeToRowNum(t[b])
            p2 = int((p1 + p3) / 2)
            v1, v2 = np.mean(v[p1:p2]), np.mean(v[p2:p3])
            print(v1, v2)
            if v1 > v2:  # 为减速窗口
                gamaTemp_ += np.pi
                if gamaTemp_ > np.pi:
                    gamaTemp_ -= 2 * np.pi
                logFile.write('减速')
            else:  # 加速窗口
                logFile.write('加速')
            gamaTemp_ = gamaTemp_ / np.pi * 180
            gamaTemp_ = int(angelTrans(gamaTemp_))
            logFile.write('事件开始时间：' + str(int(t[a] / 60)) + ':' + str(
                int(t[a] % 60)) + '  gama角：' + str(gamaTemp_) + '\n')
            gamaTemp.append(gamaTemp_)
        logFile.write('\n')
        low = high
    gamaFile.write(str(gamaTemp) + '\n')
    gama.append(gamaTemp)
print('complete1')
