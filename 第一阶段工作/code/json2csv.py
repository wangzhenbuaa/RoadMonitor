import json
import csv
#import jsonpath

infile = open('19e80_1.json', 'r')
outfile = open('19e80_1.csv', 'w',newline='')

data = json.load(infile)
# key_list = ['latitude', 'longitude', 'trip', 'x', 'y', 'z', 'result', 'time', 'key', 'color']
writer = csv.writer(outfile)
data_columns = []
# writer.writerow(key_list)
# return False
# for key in key_list:
#     column = jsonpath.jsonpath(data,'$..'+key)
#     data_columns.append(column)
#     print(len(column))
#     print('*'*20)
if isinstance(data, list):
    print('list')
    title = []
    title_finish = True
    rows = []
    for item in data:
        #         print('item', item)
        row_data = []
        for key in item:
            #             print(key, item[key])
            if isinstance(item[key], dict):
                sub_data = item[key]
                for sub in sub_data:
                    row_data.append(sub_data[sub])
                    if title_finish:
                        title.append(sub)
            else:
                row_data.append(item[key])
                if title_finish:
                    title.append(key)
        #         rows.append(row_data)
        if title_finish:
            writer.writerow(title)
            print('title', title)
        title_finish = False
        writer.writerow(row_data)
        print('data',row_data )
    #         print('*'*60)
    print('title', title)
else:#data is a dict
    title = []
    title_finish = True
    for item in data:#item: first layer
        print('dict')
        sub_data = data[item]#sub_data is a list
        print('ss',item)
        for sub_item in sub_data:#sub_item is a dict: second layer
            #print('sub_item',sub_item)
            row_data = []
            for key in sub_item:#key is color,coordinate and so on
                #             print(key, sub_item[key])
                if isinstance(sub_item[key], dict):#if key==coordinate,then sub_item[key] is a dict
                    sub_data = sub_item[key]
                    for sub in sub_data:#sub= longitute and latitude
                        row_data.append(sub_data[sub])#add value of longitude and latitude to row_data
                        if title_finish:
                            title.append(sub)#add longitude, latitude to title
                else:
                    row_data.append(sub_item[key])#add value of color,gyroscopeX and so on to raw_data
                    if title_finish:
                        title.append(key)#add color, gyroscopeX and so on to title
            #         rows.append(row_data)
            if title_finish:
                writer.writerow(title)
                print('title', title)
            title_finish = False
            writer.writerow(row_data)
            print('data',row_data )
            print('-'*60)
        print('*'*60)

outfile.close()
