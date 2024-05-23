import requests
import csv
import json
import time
import wbi

img_key, sub_key = wbi.getWbiKeys()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Origin': 'https://space.bilibili.com',
    'Connection': 'keep-alive',
    'Referer': 'https://space.bilibili.com/546195/fans/fans',
    'Cache-Control': 'max-age=0',
    'cookie': "buvid3=51EC002A-20D3-5382-D942-D06DAFCC03EE25241infoc; b_nut=1701741925; i-wanna-go-back=-1; b_ut=7; _uuid=5CD54E68-4E109-7EB3-4E93-B6133710C4106825145infoc; enable_web_push=DISABLE; buvid4=48819C9D-BFB2-3AD8-FD64-9A26B8ECF6CD39245-022090614-PFJkqvvsrkodK2nau9jSVg==; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(mmkYYmuYu0J'u~|u~Rk||J; buvid_fp_plain=undefined; hit-dyn-v2=1; DedeUserID=163004010; DedeUserID__ckMd5=9fa28f62f412dc2b; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_QUALITY=80; bp_video_offset_163004010=925309906047729762; home_feed_column=5; PVID=1; browser_resolution=1536-712; fingerprint=ce2e86c39d090ec82ebbbd064a59c679; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTY1NDc4NTEsImlhdCI6MTcxNjI4ODU5MSwicGx0IjotMX0.DpACwtK4pYN1k6R-QRio9yWCiynJ8H9LxMZOdZtWJsc; bili_ticket_expires=1716547791; SESSDATA=8c6b0950,1731905824,0f46c*51CjDfcEnKKACLNTD3A51J7NZp5rr-1HOd-ldKUCfDEgsBUJ3OIb8RLeQ14vYcd392Jx4SVndZUzFDbnFoczZwSHluTzcxMWJSZjJIQ1F2UmxwNGpkRUk4dUU1LTdpb1J1bTJuR1BoUVRtb2cwNFgxRFdabGZqcXhLVzlVaFZaQ2tENGdDRTlYNTJ3IIEC; bili_jct=8cfca3c687ab5cc98fadfed8c0510a2e; bp_t_offset_163004010=934238498819407891; b_lsid=4E49FE7E_18FA1084A0F; buvid_fp=51EC002A-20D3-5382-D942-D06DAFCC03EE25241infoc"
}


# 获取用户详细信息
def getUserDetails(mid):
    signed_params = wbi.encWbi(
        params={
            'mid': mid
        },
        img_key=img_key,
        sub_key=sub_key
    )
    res = requests.get('https://api.bilibili.com/x/space/wbi/acc/info', headers=headers, params=signed_params)
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
        json_obj = json.loads(fansDetails.text)
        sex = json_obj['data']['sex']
        print("uid：" + str(fans_mid), "关注时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),"用户名：" + uname, "性别：" + str(sex))
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