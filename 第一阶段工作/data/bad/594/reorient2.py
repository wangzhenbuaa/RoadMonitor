import numpy as np
import pandas as pd
import math
import glob

path = './ACCL/new1/*.csv'
strTemp = path[:-10]
dataList = glob.glob(path)
numFile = len(dataList)
print('to solve %d files' % numFile)
gamaList1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
gamaList2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
gamaList3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
gamaList4 = [0, 0, 0, 0, 0, 0]
gamaL = [gamaList1, gamaList2, gamaList3, gamaList4]

for fileIndex in range(numFile):
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    print(data.shape)
    x1 = data['x1']
    y1 = data['y1']
    z1 = data['z1']
    x2, y2, z2 = [], [], []
    gamaList = gamaL[fileIndex]
    segSize = int(len(x1) / len(gamaList))
    last = 0
    # 坐标转换
    for i in range(len(x1)):
        gama = gamaList[min(int(i / segSize), len(gamaList) - 1)]
        # 输出验证信息
        if gama != last:
            print('gama', gama)
            last = gama

        gama = gama / 180 * math.pi
        x_2 = x1[i] * math.cos(gama) - y1[i] * math.sin(gama)
        y_2 = y1[i] * math.cos(gama) + x1[i] * math.sin(gama)
        x2.append(x_2)
        y2.append(y_2)

    data_new = {}
    data_new['time'] = data['time']
    data_new['x'] = data['x']
    data_new['y'] = data['y']
    data_new['z'] = data['z']
    data_new['x1'] = data['x1']
    data_new['y1'] = data['y1']
    data_new['z1'] = data['z1']
    data_new['x2'] = x2
    data_new['y2'] = y2
    data_new['z2'] = data['z1']

    name = strTemp + 'new2/d37e6_acc_' + str(fileIndex + 1) + '.csv'
    data_new = pd.DataFrame(data_new)
    data_new.to_csv(name, index=False)
    print(np.mean(x2), np.mean(y2), np.mean(z2))
    print('ok')
