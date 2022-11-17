import time
import requests
import csv
import math
import json as json

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
# 请求头
# 'Referer': 'https://space.bilibili.com/546195/fans/fans',
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Origin': 'https://space.bilibili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'referer': 'https://space.bilibili.com/163004010?spm_id_from=333.1007.0.0',
    'cookie': 'buvid3=E946D92C-82FA-A965-9B0E-A7BF9B4FC3DD37201infoc; i-wanna-go-back=-1; '
              '_uuid=6DB6715B-CFAE-3D7E-10F9C-FDFF14B667E237159infoc; '
              'buvid4=48819C9D-BFB2-3AD8-FD64-9A26B8ECF6CD39245-022090614-PFJkqvvsrkodK2nau9jSVg==; '
              'buvid_fp_plain=undefined; b_ut=5; b_nut=100; hit-dyn-v2=1; nostalgia_conf=-1; '
              'LIVE_BUVID=AUTO4816633296181216; CURRENT_QUALITY=80; hit-new-style-dyn=0; DedeUserID=163004010; '
              'DedeUserID__ckMd5=9fa28f62f412dc2b; CURRENT_FNVAL=4048; PVID=1; SESSDATA=8a32740e,1683707055,'
              '4c0c0*b1; bili_jct=9711c0fcfbf8d9709266ca110a229f43; sid=7be7372l; '
              'fingerprint=a4c2f8e998556d660f20d241a0d98cfa; buvid_fp=8c65888b35583fa3e532447581e582dd; '
              'bp_video_offset_163004010=727230270818746400; b_lsid=752FD4106_18466FD77C5; innersign=0 '
}


# 获取该用户关注列表中的用户
def getNextUsers(userId):
    follow_text = requests.get("https://api.bilibili.com/x/relation/followings?vmid={}&pn=1".format(userId),
                               headers=header).text
    follow_json = json.loads(follow_text)
    # 筛选未设置隐私的用户
    if follow_json['code'] != 0:
        return []
    else:
        # 关注人数
        follow_num = follow_json['data']['total']
        # 获取pn数
        pns = math.ceil(follow_num / 50)
        urls = ["https://api.bilibili.com/x/relation/followings?vmid={}&pn={}".format(userId, i) for i in
                range(1, pns + 1)]
        follow_data = []
        for url in urls:
            text = requests.get(url, headers=header).text
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
    while True:
        url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={n}&keyword=&order=pubdate&jsonp' \
              f'=jsonp '
        r = requests.get(url, headers=header)
        _json = json.loads(r.text)
        v_list = _json.get('data').get('list').get('vlist')
        n += 1
        if len(v_list) != 0:  # 程序终止标志
            result = []
            for video in v_list:
                once = []
                video_title = video.get('title')  # 标题
                video_aid = video.get('aid')  # av号
                video_bvid = video.get('bvid')  # BV号
                # video_play_num = video.get('play')  # 播放数量
                # video_comment_num = video.get('comment')  # 当前评论数量
                # video_danmu_num = video.get('video_review')  # 弹幕数量
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
        else:
            print(f'[----------------------------爬取了{id_num - 1}个视频----------------------------]')
            print('用户{}的视频信息爬取完毕！\n'.format(uid))
            # 只返回aid那一列
            return result, [i[1] for i in result]


def upVideoDetail(aid):
    url = r'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(aid)
    # 获取url
    response = requests.get(url, timeout=30, headers=header)
    text = response.text
    jsonobj = json.loads(text)

    # 从Json对象获取视频基本信息并转入词典中
    video_dict = {'aid': jsonobj['data']['aid'],
                  'bvid': jsonobj['data']['bvid'],
                  'view': jsonobj['data']['view'],
                  'danmuku_num': jsonobj['data']['danmaku'],
                  'reply_num': jsonobj['data']['reply'],
                  'favorite_num': jsonobj['data']['favorite'],
                  'coin_num': jsonobj['data']['coin'],
                  'share_num': jsonobj['data']['share'],
                  'like_num': jsonobj['data']['like']
                  }
    # 直接返回aid,view,danmuku_num,reply_num,favorite_num,coin_num,share_num,like_num
    return [video_dict['aid'], video_dict['view'], video_dict['danmuku_num'], video_dict['reply_num'], video_dict['favorite_num'], video_dict['coin_num'], video_dict['share_num'], video_dict['like_num']]


def upSumVideoDetail(uid):
    print('upSumVideoDetail()')
    print('正在获取用户{}的视频详细信息...'.format(uid))
    _, result = upVideo(uid)
    temp = []
    for i in result:
        temp.append(upVideoDetail(i))
        time.sleep(1)
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
    r1 = requests.get(url1, headers=header)
    r2 = requests.get(url2, headers=header)
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
    res = getOverview(uid)
    print(res)
    # writeOverview_csv(res, uid)

    # upSumVideo(uid)

    # upSumVideoDetail(uid)


