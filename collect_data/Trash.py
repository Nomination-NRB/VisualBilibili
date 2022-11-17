import os


# 获得当前目录下的文件名字
def getName(folder):
    return folder, list(os.listdir(folder))


# 删除csv文件
def deleteCSV(singelfolder, filelist):
    backuppath = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Data'
    newdir = os.getcwd() + '/' + singelfolder
    os.chdir(singelfolder)
    for file in filelist:
        if file.endswith('.csv'):
            os.remove(file)
    os.chdir(backuppath)


def mydelete():
    # 获得当前目录列表
    newpath = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Data'
    _, filelist = getName(newpath)
    for folder in filelist:
        temppath = newpath + '/' + folder
        singelfolder, singelfilelist = getName(temppath)
        # print(filepath)
        deleteCSV(singelfolder, singelfilelist)
        print('已删除' + singelfolder + '文件夹的csv文件')
    print('删除完毕')


if __name__ == "__main__":
    mydelete()
