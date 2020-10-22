import numpy as np
import pandas as pd
from scipy import signal
import glob

path = './ACCL/new2/*.csv'
strTemp = path[:-10]
dataList = glob.glob(path)
numFile = len(dataList)
print('to solve %d files' % numFile)

for fileIndex in range(numFile):
    data = pd.read_csv(dataList[fileIndex], encoding='utf-8')
    print(data.shape)
    x2 = data['x2']
    y2 = data['y2']
    z2 = data['z2']
    xFilter, yFilter, zFilter = [], [], []
    # 巴特沃斯滤波器参数分别为阶数，第二个参数=2*截止频率/采样频率 2*2/50=0.12
    # highpass
    b_high, a_high = signal.butter(11, 0.08, 'highpass')
    # b_high, a_high = signal.butter(11, [0.1, 0.9], 'highpass')
    xFilter = signal.filtfilt(b_high, a_high, x2)
    yFilter = signal.filtfilt(b_high, a_high, y2)
    zFilter = signal.filtfilt(b_high, a_high, z2)

    data_new = {}
    data_new['time'] = data['time']
    data_new['x'] = data['x']
    data_new['y'] = data['y']
    data_new['z'] = data['z']
    data_new['x1'] = data['x1']
    data_new['y1'] = data['y1']
    data_new['z1'] = data['z1']
    data_new['x2'] = data['x2']
    data_new['y2'] = data['y2']
    data_new['z2'] = data['z2']
    data_new['xFilter'] = xFilter
    data_new['yFilter'] = yFilter
    data_new['zFilter'] = zFilter

    name = strTemp + 'new3/d37e6_acc_594_' + str(fileIndex + 1) + '.csv'
    data_new = pd.DataFrame(data_new)
    data_new.to_csv(name, index=False)
    print(np.mean(xFilter), np.mean(yFilter), np.mean(zFilter))
    print('complete')
