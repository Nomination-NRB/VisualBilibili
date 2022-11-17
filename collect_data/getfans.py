import requests
import csv
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Origin': 'https://space.bilibili.com',
    'Connection': 'keep-alive',
    'Referer': 'https://space.bilibili.com/546195/fans/fans',
    'Cache-Control': 'max-age=0',
    'cookie': 'buvid3=E946D92C-82FA-A965-9B0E-A7BF9B4FC3DD37201infoc; i-wanna-go-back=-1; '
              '_uuid=6DB6715B-CFAE-3D7E-10F9C-FDFF14B667E237159infoc;buvid4=48819C9D-BFB2-3AD8-FD64-9A26B8ECF6CD39245'
              '-022090614-PFJkqvvsrkodK2nau9jSVg==; rpdid=|(k~Rkmkmlmk0J\'uYYkRRYu|Y; buvid_fp_plain=undefined; '
              'b_ut=5; b_nut=100; hit-dyn-v2=1; nostalgia_conf=-1; LIVE_BUVID=AUTO4816633296181216; '
              'CURRENT_QUALITY=80; hit-new-style-dyn=0; DedeUserID=163004010; DedeUserID__ckMd5=9fa28f62f412dc2b; '
              'CURRENT_FNVAL=4048; PVID=1; SESSDATA=628dc03f,1683618623,e0a80*b1; '
              'bili_jct=8c9882c3b60d3a8f7025816277eca741; sid=7qwt7q7x; bp_video_offset_163004010=726775098777796600; '
              'fingerprint=a4c2f8e998556d660f20d241a0d98cfa; buvid_fp=092efab84206a7bcc7fdea557cfeeca4; '
              'b_lsid=216CC7C1_18461CFCBA0; innersign=0 '
}


# 获取用户详细信息
def getUserDetails(mid):
    res = requests.get('https://api.bilibili.com/x/space/acc/info?mid=' + str(mid) + '&jsonp=jsonp', headers=headers)
    return res


# 获取uid的粉丝列表
def getFans(uid):
    # uid = '163004010'
    # uid = '237733293'
    print('getFans()')
    print('正在获取用户{}的粉丝列表...'.format(uid))
    response = requests.get('https://api.bilibili.com/x/relation/followers?vmid={}&pn=1&ps=200'.format(uid),
                            headers=headers)
    responseData = json.loads(response.text)
    res = []
    for entry in responseData['data']['list']:
        temp = []
        # 如果字典中有'mtime'键，则将entry['mtime']的值赋给mtime，否则赋值为当前系统时间
        mtime = entry['mtime'] if 'mtime' in entry else time.time()
        uname = entry['uname'] if 'uname' in entry else '无名氏'
        fans_mid = entry['mid'] if 'mid' in entry else '0'
        fansDetails = getUserDetails(fans_mid)
        time.sleep(1)
        json_obj = json.loads(fansDetails.text)
        sex = json_obj['data']['sex']
        # print("uid：" + str(fans_mid), "关注时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),
        #       "用户名：" + uname, "性别：" + str(sex))
        temp.append(fans_mid)
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)))
        temp.append(uname)
        temp.append(sex)
        res.append(temp)
    print('获取用户{}的粉丝列表完成！\n'.format(uid))
    return res


# 将粉丝列表写入文件
def writeFansListToFile(fansList, uid):
    print('writeFansListToFile()')
    print('正在将用户{}的粉丝列表写入Data/fansData...'.format(uid))
    with open('../Data/fansData/{}_fans_data.csv'.format(uid), 'w', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        # uid, time, name, sex
        title = ['uid', 'time', 'name', 'sex']
        writer.writerow(title)
        for entry in fansList:
            writer.writerow(entry)
    print('将用户{}的粉丝列表写入Data/fansData完成！\n'.format(uid))


if __name__ == '__main__':
    uid = '163004010'
    result = getFans(uid)
    # writeFansListToFile(result, uid)
    print(result)