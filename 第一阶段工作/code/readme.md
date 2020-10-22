本部分为代码部分。有的是基于notebook的ipython，有的是.py文件<br>
pre1:<br>
1、排序 sort_phoneData<br>
将手机数据行记录按时间先后排序<br>
<br>
2、分割1 segment1<br>
将一天的数据分成每次实验的数据<br>
<br>
3、重写 rewrite_phone<br>
此步骤前需根据手机和相机的波形，将两者时间对齐，得到时间差<br>
将数据重组，并在时间轴上平移<br>
<br>
4、分割2 segment2<br>
将一次实验的数据分割成与相机数据同大小的文件，便于标记<br>
<br>
pre2:
由于要批量处理文件，用pycharm写的，置于各数据文件目录下<br>
1、重采样 resampling.py<br>
2、坐标转换1 reorinet1.py<br>
3、坐标转换2 calcuGama.py, reorien2.py<br>
4、滤波 highpass Threshold = 2Hz  filter.py<br>
由此得到new3文件夹下的各轴数据<br>
<br>
pre3：<br>
datasetsGenerator.py生成数据集<br>
<br>
post：<br>
进行特征提取，模型训练及测试<br>
<br>
drawing：<br>
论文绘图<br>
