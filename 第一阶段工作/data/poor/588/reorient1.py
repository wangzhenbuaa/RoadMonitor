import numpy as np
import pandas as pd
import math
import glob


# alpha [-pi,pi],  beta [-pi/2,pi/2]
def calcuAngle1(x, y, z):
    alpha = math.atan2(y, z)
    beta = math.atan(-x / math.sqrt(y * y + z * z))
    return alpha, beta


def trans1(alpha, beta, x0, y0, z0):
    x1 = math.cos(beta) * x0 + math.sin(beta) * math.sin(alpha) * y0 + math.cos(alpha) * math.sin(beta) * z0
    y1 = math.cos(alpha) * y0 - math.sin(alpha) * z0
    z1 = -math.sin(beta) * x0 + math.cos(beta) * math.sin(alpha) * y0 + math.cos(beta) * math.cos(alpha) * z0
    return x1, y1, z1


path = './ACCL/new/*.csv'
strTemp = path[:-9]
dataList = glob.glob(path)
numFile = len(dataList)
print('to solve %d files' % numFile)
for fileIndex in range(numFile):
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    print(data.shape)
    x = data['x']
    y = data['y']
    z = data['z']
    x1, y1, z1 = [], [], []

    # trans1
    # 假设2min内手机姿态不变，对应6000rows
    # 以样本数划分窗口
    winSize = 6000
    idx, low, high = 0, 0, 0  # low, high大窗口边界
    x_mean, y_mean, z_mean = 0, 0, 0
    alpha, beta = 0, 0
    for idx in range(len(x)):
        # find a large window
        if idx >= high:
            low = high
            high = min(high + winSize, len(x))
            # -----------------------------或直接取np.mean[low:high]
            # 滑动窗口法find the most steady small window in large window
            smallWinSize = 300
            slidingStep = 100  # 滑动步长
            left, right = low, low  # 小窗口边界
            left_s, right_s = low, low  # 稳定的小窗口边界
            min_std = 1e10
            # print('-------------')
            while right < high:
                right = min(left + smallWinSize, high)
                all_std = 1000 * (np.std(x[left:right]) + np.std(y[left:right]) + np.std(z[left:right])) / (
                        right - left)
                # print(left,' ',right,' ',all_std)
                if all_std < min_std:
                    min_std = all_std
                    left_s = left
                    right_s = right
                left += slidingStep
            x_mean = np.mean(x[left_s:right_s])
            y_mean = np.mean(y[left_s:right_s])
            z_mean = np.mean(z[left_s:right_s])
            # print(min_std,' ',left_s,' ',right_s,' ',low,' ',high)

            # -----------------------------或直接取np.mean[low:high]
            '''
            x_mean=np.mean(x[low:high])
            y_mean=np.mean(y[low:high])
            z_mean=np.mean(z[low:high])
            '''
            alpha, beta = calcuAngle1(x_mean, y_mean, z_mean)
        # x_1,y_1,z_1为第一次转换后的加速度值
        x_1, y_1, z_1 = trans1(alpha, beta, x[idx], y[idx], z[idx])
        x1.append(x_1)
        y1.append(y_1)
        z1.append(z_1)

    data_new = {}
    data_new['time'] = data['time']
    data_new['x'] = x
    data_new['y'] = y
    data_new['z'] = z
    data_new['x1'] = x1
    data_new['y1'] = y1
    data_new['z1'] = z1

    name = strTemp + 'new1/d37e6_acc_' + str(fileIndex + 3) + '.csv'
    data_new = pd.DataFrame(data_new)
    data_new.to_csv(name, index=False)
    print(np.mean(x1), np.mean(y1), np.mean(z1))
    print('ok')
