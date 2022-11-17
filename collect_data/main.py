import getBVid
import getReview
import getfans
import getUserInfo


if __name__ == "__main__":
    # 输入某个用户的uid
    uid = '237733293'

    # 获得该用户总览信息：关注数，粉丝数，播放数，阅读数
    # 输出：[90, 349, 256766, 0]
    overViewlist = getUserInfo.getOverview(uid)
    getUserInfo.writeOverview_csv(overViewlist, uid)

    # 获得该用户的粉丝列表
    # 输出：[[1817063775, '2022-11-01 23:38:40', 'bili_1817063775', '保密']]
    fansList = getfans.getFans(uid)
    getfans.writeFansListToFile(fansList, uid)

    # 获得该用户的简要视频信息
    getUserInfo.upSumVideo(uid)
    # 获得该用户的详细视频信息
    getUserInfo.upSumVideoDetail(uid)

    # 获得该用户的视频BV号
    bvlist = getBVid.getBVidMain()
    # 获得每个视频BV的评论
    getReview.getReviewMain(bvlist)
