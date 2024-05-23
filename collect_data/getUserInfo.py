import time
import requests
import csv
import math
import wbi
import json

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
img_key, sub_key = wbi.getWbiKeys()


# 请求头
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

# 获取该用户关注列表中的用户
def getNextUsers(userId):
    follow_text = requests.get("https://api.bilibili.com/x/relation/followings?vmid={}&pn=1".format(userId),
                               headers=headers).text
    follow_json = json.loads(follow_text)
    # 筛选未设置隐私的用户
    if follow_json['code'] != 0:
        return []
    else:
        # 关注人数
        follow_num = follow_json['data']['total']
        # 获取pn数
        pns = math.ceil(follow_num / 50)
        urls = ["https://api.bilibili.com/x/relation/followings?vmid={}&pn={}".format(userId, i) for i in range(1, pns + 1)]
        follow_data = []
        for url in urls:
            text = requests.get(url, headers=headers).text
            j = json.loads(text)
            try:
                user_list = j['data']['list']
                flag1 = 0
                for user in user_list:
                    # 判断是否为认证用户
                    # if user['official_verify']['type'] == 0:
                    mid = user['mid']
                    uname = user['uname']
                    sign = user['sign']
                    follow_data.append([mid, uname, sign])
                    flag1 += 1
                #         if flag1 == 10:
                #             break
                # if flag1 == 10:
                #     break
            except:
                follow_data += []
        return follow_data


def write_follow_csv(follow_uid_data, uid):
    with open('../Data/{}_follow_data.csv'.format(uid), 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # uid name sign
        # 将以上字段写入csv文件
        titlearray = ['uid', 'name', 'sign']
        writer.writerow(titlearray)
        for item in follow_uid_data:
            item[2] = item[2].replace('\n', ' ')
            if item[2] == '':
                item[2] = '无'
        writer.writerows(follow_uid_data)


def write_video_csv(video_data, uid):
    print('write_video_csv()')
    print('正在写入{}的视频信息'.format(uid))
    with open('../Data/videoData/{}_video_data.csv'.format(uid), 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # title aid bvid play comment barrage createTime timelength description link
        # 将以上字段写入csv文件
        titlearray = ['title', 'aid', 'bvid', 'createTime', 'timelength', 'description',
                      'link']
        writer.writerow(titlearray)
        for item in video_data:
            # 将item[-2]中的特殊字符替换为空格
            item[-2] = item[-2].replace('\n', ' ')
            item[-2] = item[-2].replace('\r', ' ')
            item[-2] = item[-2].replace('\t', ' ')
            if item[-2] == '':
                item[-2] = '无'
        writer.writerows(video_data)
    print('用户{}的视频信息写入完毕\n'.format(uid))


def write_videoDetail_csv(videoDetail_data, uid):
    print('write_videoDetail_csv()')
    print('正在写入{}的视频详细信息'.format(uid))
    with open('../Data/videoDetailData/{}_videoDetail_data.csv'.format(uid), 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # aid,view,barrage_num,reply_num,favorite_num,coin_num,share_num,like_num
        # 将以上字段写入csv文件
        titlearray = ['aid', 'view', 'barrage_num', 'reply_num', 'favorite_num', 'coin_num', 'share_num', 'like_num']
        writer.writerow(titlearray)
        writer.writerows(videoDetail_data)
    print('用户{}的视频详细信息写入完毕\n'.format(uid))


def upVideo(uid):
    print('upVideo()')
    print('正在获取用户{}的视频信息...'.format(uid))
    n = 1
    id_num = 1
    signed_params = wbi.encWbi(
        params={
            'mid': uid
        },
        img_key=img_key,
        sub_key=sub_key
    )
    url = 'https://api.bilibili.com/x/space/wbi/arc/search'
    r = requests.get(url, params=signed_params, headers=headers)
    _json = json.loads(r.text)
    v_list = _json.get('data').get('list').get('vlist')
    n += 1
    result = []
    for video in v_list:
        once = []
        video_title = video.get('title')  # 标题
        video_aid = video.get('aid')  # av号
        video_bvid = video.get('bvid')  # BV号
        video_created_ = video.get('created')  #
        timeArray = time.localtime(video_created_)
        video_created = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 时间字符串格式化
        video_length = video.get('length')  # 视频长度
        video_description = video.get('description')  # 视频描述
        video_link = 'https://www.bilibili.com/video/' + video_bvid  # 链接地址：固定开头+BV号
        id_num += 1
        once.append(video_title)
        once.append(video_aid)
        once.append(video_bvid)
        once.append(video_created)
        once.append(video_length)
        once.append(video_description)
        once.append(video_link)
        result.append(once)
        print(f'已爬取{id_num - 1}个视频 => {video_title} {video_created}')

    print(f'[----------------------------爬取了{id_num - 1}个视频----------------------------]')
    print('用户{}的视频信息爬取完毕！\n'.format(uid))
    # 只返回aid那一列
    return result, [i[1] for i in result]


def upVideoDetail(aid):
    url = r'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
    # 获取url
    response = requests.get(url, timeout=30, headers=headers)
    text = response.text
    jsonobj = json.loads(text)
    # 从Json对象获取视频基本信息并转入词典中
    video_dict = {'aid': jsonobj['data']['aid'],
                  'bvid': jsonobj['data']['bvid'],
                  'view': jsonobj['data']['stat']['view'],
                  'danmuku_num': jsonobj['data']['stat']['danmaku'],
                  'reply_num': jsonobj['data']['stat']['reply'],
                  'favorite_num': jsonobj['data']['stat']['favorite'],
                  'coin_num': jsonobj['data']['stat']['coin'],
                  'share_num': jsonobj['data']['stat']['share'],
                  'like_num': jsonobj['data']['stat']['like']
                  }
    # 直接返回aid,view,danmuku_num,reply_num,favorite_num,coin_num,share_num,like_num
    return [video_dict['aid'], video_dict['view'], video_dict['danmuku_num'], video_dict['reply_num'], video_dict['favorite_num'], video_dict['coin_num'], video_dict['share_num'], video_dict['like_num']]


def upSumVideoDetail(uid):
    print('upSumVideoDetail()')
    print('正在获取用户{}的视频详细信息...'.format(uid))
    _, result = upVideo(uid)
    temp = []
    for index, i in enumerate(result):
        temp.append(upVideoDetail(i))
        print('已爬取uid={} aid={}的视频详细信息，第{}个视频'.format(uid, i, index + 1))
    write_videoDetail_csv(temp, uid)


def upSumVideo(uid):
    print('upSumVideo()')
    print('正在获取用户{}的视频信息...'.format(uid))
    result, _ = upVideo(uid)
    write_video_csv(result, uid)


# 获取up的总关注数，粉丝数，播放数，阅读数
def getOverview(uid):
    print('getOverview()')
    print('正在获取用户{}的总关注数，粉丝数，播放数，阅读数...'.format(uid))
    url1 = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(uid)
    url2 = 'https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp'.format(uid)
    r1 = requests.get(url1, headers=headers)
    r2 = requests.get(url2, headers=headers)
    json1 = json.loads(r1.text)
    json2 = json.loads(r2.text)
    # 关注数
    following = json1.get('data').get('following')
    # 粉丝数
    follower = json1.get('data').get('follower')
    # 播放数
    archive_view = json2.get('data').get('archive').get('view')
    # 阅读数
    article_view = json2.get('data').get('article').get('view')
    # 获赞数
    likes = json2.get('data').get('likes')
    print('用户{}的总关注数，粉丝数，播放数，阅读数，获赞数获取完成！\n'.format(uid))
    return [following, follower, archive_view, article_view, likes]


def writeOverview_csv(overview, uid):
    print('writeOverview_csv()')
    print('正在写入用户{}的总关注数，粉丝数，播放数，阅读数...'.format(uid))
    with open('../Data/overViewData/{}_overview_data.csv'.format(uid), 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        title = ['following', 'follower', 'play_view', 'article_view', 'likes']
        writer.writerow(title)
        writer.writerow(overview)
    print('用户{}的总关注数，粉丝数，播放数，阅读数，获赞数写入完成！\n'.format(uid))


if __name__ == '__main__':
    # uid = '163004010'
    uid = '237733293'
    # res = getNextUsers(uid)
    # print(res)
    # res = getOverview(uid)
    # print(res)
    # writeOverview_csv(res, uid)
    # upSumVideo(uid)

    upSumVideoDetail(uid)


