import os
import time
import json
import glob
import requests
import pandas as pd
import re

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接

import wbi

img_key, sub_key = wbi.getWbiKeys()

# cookie 与 数据保存路径(默认留空为'./')
cookie = "buvid3=63B1C902-3DD5-CD46-85D8-9A69679BC65665004infoc; CURRENT_FNVAL=80; blackside_state=1; sid=6aaqymp9; " \
         "rpdid=|(u)mJ~Rlll~0J'uYkR||uuYm; fingerprint=33bf6967b63128e997c2ee0e3659a990; " \
         "buvid_fp=63B1C902-3DD5-CD46-85D8-9A69679BC65665004infoc; " \
         "buvid_fp_plain=63B1C902-3DD5-CD46-85D8-9A69679BC65665004infoc "
file_dir = "./"
# 1:评论(楼层);2:最新评论(时间);3:热门评论(热度)
comment_mode = 3


def visit(bv):
    """ 访问av/BV对应的网页,查看是否存在 """

    if bv[:2] == 'BV' or bv[:2] == 'av':
        url = 'https://www.bilibili.com/video/' + bv
        headers = {
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,
            # */*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://www.bilibili.com/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.106 Safari/537.36',
            'cookie': cookie
        }
        response = requests.get(url, headers=headers)
    else:
        print('视频不存在!')
        return 0
    if response.status_code == 404 or """<div class="error-text">啊叻？视频不见了？</div>""" in response.text:
        print('视频不存在!')
        return 0
    else:
        return 1


def Bta(bv):
    """ 将BV号转化为av号,如果已经是av号,直接返回数字部分(文本类型),方法参考cv9646821 """

    if bv[:2] == 'av':
        return bv[2:]
    bv = list(bv[2:])
    keys = {'1': 13, '2': 12, '3': 46, '4': 31, '5': 43, '6': 18, '7': 40, '8': 28, '9': 5,
            'A': 54, 'B': 20, 'C': 15, 'D': 8, 'E': 39, 'F': 57, 'G': 45, 'H': 36, 'J': 38, 'K': 51, 'L': 42, 'M': 49,
            'N': 52, 'P': 53, 'Q': 7, 'R': 4, 'S': 9, 'T': 50, 'U': 10, 'V': 44, 'W': 34, 'X': 6, 'Y': 25, 'Z': 1,
            'a': 26, 'b': 29, 'c': 56, 'd': 3, 'e': 24, 'f': 0, 'g': 47, 'h': 27, 'i': 22, 'j': 41, 'k': 16, 'm': 11,
            'n': 37, 'o': 2, 'p': 35, 'q': 21, 'r': 17, 's': 33, 't': 30, 'u': 48, 'v': 23, 'w': 55, 'x': 32, 'y': 14,
            'z': 19}
    for i in range(len(bv)):
        bv[i] = keys[bv[i]]
    bv[0] *= (58 ** 6)
    bv[1] *= (58 ** 2)
    bv[2] *= (58 ** 4)
    bv[3] *= (58 ** 8)
    bv[4] *= (58 ** 5)
    bv[5] *= (58 ** 9)
    bv[6] *= (58 ** 3)
    bv[7] *= (58 ** 7)
    bv[8] *= 58
    return str((sum(bv) - 100618342136696320) ^ 177451812)


def send_f(bv, nexts=0, mode=3):
    """ 返回父评论json  \n bv: 全bv号  \n nests: json页码  \n mode: 1楼层,2时间,3热门 """

    if nexts == -1:
        return 0

    # 为给定的参数生成签名
    signed_params = wbi.encWbi(
        params={
            'oid': bv,
            'type': 1
        },
        img_key=img_key,
        sub_key=sub_key
    )

    # 定义URL
    url = 'https://api.bilibili.com/x/v2/reply'

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

    response = requests.get(url, params=signed_params, headers=headers)
    response.encoding = 'utf-8'
    # 将得到的json文本转化为可读json
    if 'code' in response.text:
        c_json = json.loads(response.text)
    else:
        c_json = {'code': -1}
    if c_json['code'] != 0:
        print('json error!')
        print(response.status_code)
        print(response.text)
        return 0  # 读取错误
    return c_json


def send_r(aid, rpid, pn=1):
    """ 返回子评论json  \n bv: 全bv号  \n rpid: 父评论的id  \n pn: 子评论的页码 """
    # 为给定的参数生成签名
    signed_params = wbi.encWbi(
        params={
            'oid': aid,
            'type': 1
        },
        img_key=img_key,
        sub_key=sub_key
    )

    # 定义URL
    url = 'https://api.bilibili.com/x/v2/reply'

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

    response = requests.get(url, params=signed_params, headers=headers)
    response.encoding = 'utf-8'

    # 将得到的json文本转化为可读json
    if 'code' in response.text:
        cr_json = json.loads(response.text)
    else:
        cr_json = {'code': -1}
    if cr_json['code'] != 0:
        print('error!')
        print(response.status_code)
        print(response.text)
        return 0  # 读取错误
    return cr_json


def parse_comment_r(bv, rpid):
    """ 解析子评论json  \n bv: 全bv号  \n rpid: reply_id """

    cr_json = send_r(bv, rpid)['data']
    count = cr_json['page']['count']
    csv_temp = ''
    for pn in range(1, count // 10 + 2):
        print('p%d %d  ' % (pn, count), end='\r')
        cr_json = send_r(bv, rpid, pn=pn)['data']
        cr_list = cr_json['replies']
        if cr_list:  # 有时'replies'为'None'
            for i in range(len(cr_list)):
                comment_temp = {
                    'floor': '0',
                    'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cr_list[i]['ctime'])),  # 时间
                    'like': cr_list[i]['like'],  # 赞数
                    'uid': cr_list[i]['member']['mid'],  # uid
                    'name': cr_list[i]['member']['uname'],  # 用户名
                    'sex': cr_list[i]['member']['sex'],  # 性别
                    'content': cr_list[i]['content']['message'],  # 子评论
                }  # 保留需要的内容\
                # print(comment_temp['content'])
                for item in comment_temp['content']:
                    if item == ',':
                        comment_temp['content'] = comment_temp['content'].replace(item, '，')
                for i in comment_temp:
                    csv_temp += str(comment_temp[i]) + ','
                csv_temp = csv_temp[:-1] + '\n'
    return csv_temp


def parse_comment_f(bv):
    """ 解析父评论json """

    c_json = send_f(bv, mode=comment_mode)
    if c_json:
        # 总评论数
        try:
            count_all = c_json['data']['page']['count']
            print('comments:%d' % count_all)
        except KeyError:
            print('该视频可能没有评论!')
            return '0', '2'  # 找不到键值
    else:
        print('json错误')
        return '1', '0'  # json错误

    csv = ''
    # 开始序号
    count_next = 0

    # 存放原始json
    all_json = ''

    for page in range(count_all // 20 + 1):
        print('page:%d' % (page + 1))

        all_json += str(c_json) + '\n'

        # 评论列表
        c_list = c_json['data']['replies']

        # 有评论,就进入下面的循环保存
        for i in range(len(c_list)):
            comment_temp = {
                # 'floor': c_list[i]['floor'],			# 楼层
                'floor': '0',  # 楼层
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(c_list[i]['ctime'])),  # 时间
                'like': c_list[i]['like'],  # 赞数
                'uid': c_list[i]['member']['mid'],  # uid
                'name': c_list[i]['member']['uname'],  # 用户名
                'sex': c_list[i]['member']['sex'],  # 性别
                'content': c_list[i]['content']['message'],  # 评论内容
            }  # 保留需要的内容
            # 若有子评论,记录rpid,爬取子评论
            replies = False
            if c_list[i]['rcount'] or ('replies' in c_list[i] and c_list[i]['replies']):
                replies = True
                rpid = c_list[i]['rpid']

            for item in comment_temp['content']:
                if item == ',':
                    comment_temp['content'] = comment_temp['content'].replace(item, '，')

            for i in comment_temp:
                csv += str(comment_temp[i]) + ','
            csv = csv[:-1] + '\n'

    return csv, all_json


def review(aid, file_dir="../Data/reviewData/"):
    print('正在爬取视频%s的评论' % aid)
    
    # 处理存储路径
    if file_dir == '':
        file_dir = './'
    elif file_dir[-1] != '/' or file_dir[-1] != '/':
        file_dir += '/'
    if not os.path.exists(file_dir):
        print('存储路径不存在...', end='')
        os.mkdir(file_dir)
        print('已自动创建!')

    dir_csv = file_dir + aid + '.csv'
    
    # 如果是第一次写入文件,创建并写入标题
    if not os.path.exists(dir_csv):
        with open(dir_csv, 'w', encoding='utf-8-sig') as fp:
            fp.write('tag,time,approve,uid,name,sex,review\n')

    csv, all_json = parse_comment_f(aid)
    # 保存评论csv
    while True:
        try:
            with open(dir_csv, 'a', encoding='utf-8') as fp:
                if csv == '0':
                    temp = '0,0000-00-00 00:00:00,0,000000000,姓名,性别,无\n'
                    fp.write(temp)
                else:
                    fp.write(csv)
            print('视频{}评论保存完毕!\n'.format(aid))
            break
        except PermissionError:
            input('文件被占用!!!(关闭占用的程序后,回车重试)')


# 判断csv文件中的每一行的第一个值是不是0，如果是0，则删除这一行
def deleteIllegal(file_dir='../Data/reviewData/'):
    print('deleteIllegal()')
    print('正在删除非法评论...')
    file_list = glob.glob(file_dir + '*.csv')
    for file in file_list:
        df = pd.read_csv(file)
        # 判断开头是不是0
        rowlength = df.shape[0]
        for i in range(rowlength):
            if str(df.loc[i, "tag"]) != '0':
                # print(df.loc[i, "tag"])
                df = df.drop(i)
                df.to_csv(file, index=False, encoding='utf-8')
    print('删除完毕！\n')


# 将多个csv文件合并为一个文件，并设置一个表头
def merge_csv(file_dir='../Data/reviewData/'):
    print('merge_csv()')
    file_list = glob.glob(file_dir + '*.csv')
    print('共发现%s个CSV文件' % len(file_list))
    # 创建一个空的dataframe
    df = pd.DataFrame()
    for file in file_list:
        df = df.append(pd.read_csv(file))
    df.to_csv('../Data/sumData/sumReviewData.csv', index=False, encoding='utf-8')
    print('合并完毕！\n')


# 获得sumData文件夹里的csv文件
def get_sumcsv_list():
    path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Data/sumData'
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                file_list.append(os.path.join(root, file))
    return file_list


def filter_str(desstr, restr=''):
    # 过滤除中英文及数字以外的其他字符
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)


# 将csv文件的review数据写入新的csv文件
def clean_csv(sumFileName='sumReviewData.csv'):
    print('clean_csv()')
    print('正在准备train训练数据...')
    filePath = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Data/sumData/{}'.format(sumFileName)
    df = pd.read_csv(filePath)
    # 获得review列表
    review_list = df['review'].tolist()
    review_temp = []
    for review in review_list:
        review = filter_str(review)
        if review != '无':
            review_temp.append(review)

    df = pd.DataFrame(review_temp)
    df.to_csv('../Data/reviewForInfer/review.csv', index=False)
    print('准备完毕！\n')
    return df


# 将csv文件的review数据写入新的csv文件，与上面相同，只是这个是用于测试
def write_csv(file_list):
    for file in file_list:
        df = pd.read_csv(file)
        # 获得review列表
        review_list = df['review'].tolist()
        review_temp = []
        for review in review_list:
            if review != '无':
                review_temp.append(review)
    df = pd.DataFrame(review_temp)
    df.to_csv('../Data/reviewTest.csv', index=False)
    return df


# 爬虫地址
alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'


def dec(x):  # BV号转换成AV号
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58 ** i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324


def getReviewMain(aidlist):
    for aid in aidlist:
        review(aid)
    deleteIllegal()
    merge_csv()
    clean_csv()
    print('getReview.py执行完毕！\n')


if __name__ == "__main__":
    # BV1KR4y1u7o7
    # BV1Vr4y1H7Vd
    bv = "BV1KR4y1u7o7"
    file_dir = "../Data/reviewData/"
    # review(bv, file_dir)
    # deleteIllegal(file_dir)
    # merge_csv(file_dir)

    sumFileName = 'sumReviewData.csv'
    clean_csv(sumFileName)
    print('=== over! ===')
