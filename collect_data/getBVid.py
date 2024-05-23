import re
import os
import pandas as pd


# 获取videoData文件夹下所有csv文件
def get_csv_list(file_path='../Data/videoData/'):
    result = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.csv'):
                # file_path = os.path.join(root, file)
                result.append(file)
    return result


# 获得bv号
def get_bvlist(csvlist):
    result = []
    for csv in csvlist:
        df = pd.read_csv('../Data/videoData/{}'.format(csv))
        for index, row in df.iterrows():
            bvstr = str(row['bvid'])
            result.append(bvstr)
    return result


def get_avlist(csvlist):
    result = []
    for csv in csvlist:
        df = pd.read_csv('../Data/videoData/{}'.format(csv))
        for index, row in df.iterrows():
            bvstr = str(row['aid'])
            result.append(bvstr)
    return result

def getAidMain():
    csvlist = get_csv_list()
    bvlist = get_avlist(csvlist)
    print('get_avlist()执行完毕！\n')
    return bvlist

def getBVidMain():
    csvlist = get_csv_list()
    bvlist = get_bvlist(csvlist)
    print('getBVid.py执行完毕！\n')
    return bvlist


if __name__ == "__main__":
    file_path = '../Data/videoData/'
    bvlist = getBVidMain()
    print(bvlist)
