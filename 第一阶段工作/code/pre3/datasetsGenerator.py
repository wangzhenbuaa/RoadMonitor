import numpy as np
import pandas as pd
import pywt
import glob


def timeToRowNum(time):
    return int(time * 100)


# 返回anomaly seg的左右边界及索引
def findInterval(time1, time2):
    left, right, idxNum = [], [], []
    for i in range(label.shape[0]):
        if st[i] < time1 and ed[i] >= time1:
            left.append(time1)
            if ed[i] <= time2:
                right.append(ed[i])
            else:
                right.append(time2)
            idxNum.append(i)
        if st[i] >= time1 and st[i] <= time2:
            left.append(st[i])
            if (ed[i] < time2):
                right.append(ed[i])
            else:
                right.append(time2)
            idxNum.append(i)
    return left, right, idxNum


typeDescription = {
    'normal': 0,
    'hole': 1,
    'transverse': 2
}

path1 = './label/*.csv'
path2 = './ACCL/*.csv'
path3 = './GPS5/*.csv'
labelList = glob.glob(path1)
dataList = glob.glob(path2)
gpsList = glob.glob(path3)
numFile = len(dataList)
print('to solve %d files' % numFile)
dataX, dataY, dataZ, dataLabel = [], [], [], []
poor, bad = [0, 1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11]

for fileIndex in range(numFile):
    label = pd.read_csv(labelList[fileIndex], encoding='utf-8')
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    gps = pd.read_csv(gpsList[fileIndex], encoding='utf-8')
    # print(label.shape)
    # print(data.shape)
    print(fileIndex + 1)

    st = label['time(st)']
    ed = label['time(ed)']
    x = data['xFilter']
    y = data['yFilter']
    z = data['zFilter']
    t = data['time']
    speed = gps['GPS (2D speed) [m/s]']

    # sliding windows and extracting features
    windowSize = 64  # 64个样本点为第一个窗口
    slidingStep = 32  # overlaping = 0.5
    speedThreshold = 3  # 速度阈值
    rmsThreshold = 1.2  # rms阈值
    x_zThreshold = 0.25
    low, high = 0, 0
    # 将窗口标记为anomaly的尺度,此处选了不同尺度
    markedSize = 0.5
    # 若最后剩余部分不足一个窗口，则舍弃
    while low + windowSize < data.shape[0]:
        high = low + windowSize
        # speed
        rowNum1, rowNum2 = timeToRowNum(t[low]), timeToRowNum(t[high])
        speed_mean = np.mean(speed[rowNum1:rowNum2])
        if speed_mean < speedThreshold:
            low += slidingStep
            continue

        rmsZ, rmsX, rmsY = np.sqrt(np.mean(z[low:high] ** 2)), np.sqrt(np.mean(x[low:high] ** 2)), np.sqrt(
            np.mean(y[low:high] ** 2))
        rms = rmsZ + rmsX + rmsY
        if rms < rmsThreshold:
            low += slidingStep
            continue

        #deltaX, deltaZ = np.max(x[low:high]) - np.min(x[low:high]), np.max(z[low:high]) - np.min(z[low:high])
        # 去除Transverse的情况
        if (rmsX / rmsZ) < x_zThreshold:
            low += slidingStep
            continue
        # ---------------------------------------------------------------------
        # label
        # 若anomaly时长除以窗口时长大于markedSize，则标记为anomaly,其性质取为时长占比最大的anomaly
        left, right, idxNum = findInterval(t[low], t[high])
        ans, mainIdx, maxInterval = 0, 0, 0
        severity, type = 0, 'normal'
        singleLabel = []
        for i in range(len(left)):
            ans += right[i] - left[i]
            if (right[i] - left[i]) > maxInterval:
                maxInterval = right[i] - left[i]
                mainIdx = idxNum[i]
        if ans >= markedSize:  # 时长大于markedSize
            type = label['type'][mainIdx]
            severity = label['severity'][mainIdx]
        elif ans > 0:  # 舍弃0<anomaly<markedsize的窗口
            low += slidingStep
            continue

        dataX.append(x[low:high])
        dataY.append(y[low:high])
        dataZ.append(z[low:high])
        singleLabel.append(typeDescription[type])
        singleLabel.append(severity)
        if fileIndex in poor:
            singleLabel.append(1)
        else:
            singleLabel.append(2)
        dataLabel.append(singleLabel)
        low += slidingStep

# write file
dataX = np.array(dataX)
dataY = np.array(dataY)
dataZ = np.array(dataZ)
dataLabel = np.array(dataLabel)

np.savetxt('./datasets/dataX.txt', dataX, fmt='%.03f')
np.savetxt('./datasets/dataY.txt', dataY, fmt='%.03f')
np.savetxt('./datasets/dataZ.txt', dataZ, fmt='%.03f')
np.savetxt('./datasets/dataLabel.txt', dataLabel, fmt='%d')

print('complete')
