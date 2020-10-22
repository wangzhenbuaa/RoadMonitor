import numpy as np
import pandas as pd
import math
import glob
import scipy.interpolate as spi


def timeToRowNum(time):
    low, high = min(int(time * 38), data.shape[0]), min(int(time * 47), data.shape[0])
    mid = 0
    while low < high - 1:
        mid = int((low + high) / 2)
        # print(low,mid,high)
        if t[mid] < time:
            low = mid
        else:
            high = mid
    temp = [low, mid, high]
    for ans in temp:
        if t[ans] >= time:
            return ans


def splineResample(x, y, xnew):
    return spi.splev(xnew, spi.splrep(x, y))


path = './ACCL/*.csv'
strTemp = path[:-5]
dataList = glob.glob(path)
numFile = len(dataList)
print('to solve %d files' % numFile)
for fileIndex in range(numFile):
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    print(data.shape)
    x = data['x']
    y = data['y']
    z = data['z']
    t = data['time']
    tResample, xResample, yResample, zResample = [], [], [], []
    # 滑动窗口，每次滑动1s
    timeEnd = t[len(t) - 1]
    print(timeEnd)
    totalNum = int(timeEnd * 50)
    tResample = np.linspace(0, timeEnd, totalNum)
    xResample = splineResample(t, x, tResample)
    yResample = splineResample(t, y, tResample)
    zResample = splineResample(t, z, tResample)

    data_new = {}
    data_new['time'] = tResample
    data_new['x'] = xResample
    data_new['y'] = yResample
    data_new['z'] = zResample
    name = strTemp + 'new/d37e6_acc_' + str(fileIndex + 1) + '.csv'
    data_new = pd.DataFrame(data_new)
    data_new.to_csv(name, index=False)
    print('ok')
