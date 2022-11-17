import pymysql
import csv


def get_conn(localhost='localhost', port=3306, user='root', passwd='root1234', db='visualization'):
    # 连接数据库
    config = {'host': localhost,
              'port': port,
              'user': user,
              'passwd': passwd,
              'db': db,
              "local_infile": 1
              }
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    close_conn(conn, cursor)
    return result


def createTable(tableName, sql):
    conn, cursor = get_conn()
    try:
        cursor.execute("DROP TABLE IF EXISTS " + tableName)
        cursor.execute(sql)
        close_conn(conn, cursor)
        print("Successfully create")
    except Exception as e:
        close_conn(conn, cursor)
        print(e)
        print("fail to create")


def deleteTable(tableName):
    conn, cursor = get_conn()
    try:
        cursor.execute("DROP TABLE IF EXISTS " + tableName)
        close_conn(conn, cursor)
        print("Successfully detele")
    except Exception as e:
        close_conn(conn, cursor)
        print(e)
        print("fail to create")


def writeInMySQL(fileName, tableName):
    # CSV数据导入MYSQL
    conn, cursor = get_conn()
    sql = "LOAD DATA LOCAL INFILE '{0}' INTO TABLE {1} CHARACTER SET UTF8 FIELDS TERMINATED BY ',' LINES TERMINATED BY " \
          "'\\r\\n' IGNORE 1 LINES "
    try:
        cursor.execute(sql.format(fileName, tableName))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        sql = "select * from " + tableName
        cursor.execute(sql)
        rows = cursor.fetchall()
        testdata = list(map(list, rows))
        close_conn(conn, cursor)


def getOverViewData(tableName1, tableName2):
    sql1 = "select following,follower,play_view,article_view,likes from {tableName1}".format(tableName1=tableName1)
    sql2 = "select count(*) from {tableName2}".format(tableName2=tableName2)
    result1 = query(sql1)
    result2 = query(sql2)
    return result1, result2


def getColumnData(tableName1, tableName2):
    sql1 = 'select title, view*0.1+barrage_num+reply_num+2*favorite_num+2*coin_num+1.5*share_num+0.5*like_num as ' \
           'sumGrade from {tableName1}, {tableName2} where {tableName1}.aid={tableName2}.aid order by sumGrade desc ' \
           'limit 9'.format(tableName1=tableName1, tableName2=tableName2)
    result1 = query(sql1)
    return result1


def getBarData(tableName1):
    sql1 = 'select timelength from {tableName1}'.format(tableName1=tableName1)
    result1 = query(sql1)
    timelength = []
    for item in result1:
        # 将item[0]以':'分割，分割后的第一个元素为分钟，第二个元素为秒
        time = item[0].split(':')
        # 将分钟转换为秒，加上秒，得到视频时长的秒数
        time = int(time[0]) * 60 + int(time[1])
        timelength.append(time)
    return timelength


def getFansData(tableName1):
    sql1 = 'select time, name, sex from {tableName1}'.format(tableName1=tableName1)
    result1 = query(sql1)
    # follow_time这一列只保留年月日
    follow_time = []
    for item in result1:
        item = item[0][0:10]
        follow_time.append(item)
    # result1中的follow_time列替换为follow_time
    result1 = list(map(list, result1))
    for i in range(len(result1)):
        result1[i][0] = follow_time[i]
    return result1


def getBoxData(tableName1, tableName2):
    sql1 = 'select view, barrage_num, reply_num, favorite_num, coin_num, share_num, like_num, title, ' \
           'view*0.1+barrage_num+reply_num+2*favorite_num+2*coin_num+1.5*share_num+0.5*like_num as sumGrade from {' \
           'tableName1}, {tableName2} where {tableName1}.aid={tableName2}.aid order by sumGrade desc limit 6'.format(
        tableName1=tableName1, tableName2=tableName2)
    result1 = query(sql1)
    return result1


def getCircleData(tableName1):
    sql1 = 'select result from {tableName1}'.format(tableName1=tableName1)
    result1 = query(sql1)
    # 计数result1中的0和1的个数
    count0 = 0
    count1 = 0
    for item in result1:
        if item[0] == '0':
            count0 += 1
        else:
            count1 += 1
    return count0, count1


def getPieData(tableName1):
    sql1 = 'select sum(view) as viewSum, sum(barrage_num) as barrageSum, sum(reply_num) as replySum, ' \
           'sum(favorite_num) as favoriteSum, sum(coin_num) as coinSum, sum(share_num) as shareSum, ' \
           'sum(like_num) as likeSum from {tableName1}'.format(tableName1=tableName1)
    result1 = query(sql1)
    return result1


if __name__ == "__main__":
    tablename1 = '237733293_fans_data'
    tablename2 = '237733293_video_data'
    tablename3 = '237733293_video_detail_data'
    tablename4 = '237733293_overView_data'
    # 字段1 uid,time,name,sex
    sql1 = "CREATE TABLE IF NOT EXISTS {tablename1} (uid VARCHAR(20) NOT NULL, time VARCHAR(20) NOT NULL, " \
           "name VARCHAR(20) NOT NULL, sex varchar(20) NOT NULL)".format(tablename1=tablename1)
    # 字段2 title,aid,bvid,createTime,timelength,description,link
    sql2 = "CREATE TABLE IF NOT EXISTS {tablename2} (title VARCHAR(100) NOT NULL, aid VARCHAR(20) NOT NULL, " \
           "bvid VARCHAR(20) NOT NULL, createTime VARCHAR(20) NOT NULL, timelength VARCHAR(20) NOT NULL, " \
           "description VARCHAR(100) NOT NULL, link VARCHAR(100) NOT NULL)".format(tablename2=tablename2)
    # 字段3 aid,view,barrage_num,reply_num,favorite_num,coin_num,share_num,like_num
    sql3 = "CREATE TABLE IF NOT EXISTS {tablename3} (aid VARCHAR(20) NOT NULL, view int(20) NOT NULL, " \
           "barrage_num int(20) NOT NULL, reply_num int(20) NOT NULL, favorite_num int(20) NOT NULL, " \
           "coin_num int(20) NOT NULL, share_num int(20) NOT NULL, like_num int(20) NOT NULL)".format(tablename3=tablename3)
    # 字段4 following,follower,play_view,article_view,likes
    sql4 = "CREATE TABLE IF NOT EXISTS {tablename4} (following int(20) NOT NULL, follower int(20) NOT NULL, " \
           "play_view int(20) NOT NULL, article_view int(20) NOT NULL, likes int(20))".format(tablename4=tablename4)
    createTable(tablename1, sql1)
    createTable(tablename2, sql2)
    createTable(tablename3, sql3)
    createTable(tablename4, sql4)
    writeInMySQL('../Data/fansData/237733293_fans_data.csv', tablename1)
    writeInMySQL('../Data/videoData/237733293_video_data.csv', tablename2)
    writeInMySQL('../Data/videoDetailData/237733293_videoDetail_data.csv', tablename3)
    writeInMySQL('../Data/overViewData/237733293_overview_data.csv', tablename4)

    tablename5 = '237733293_reviewresult'
    sql5 = 'CREATE TABLE {tablename5} (review VARCHAR(255), result VARCHAR(255))'.format(tablename5=tablename5)
    createTable(tablename5, sql5)
    filepath1 = '../Data/reviewForInfer/result.csv'
    filepath2 = '../Data/reviewForInfer/review.csv'
    # 读取result.csv文件和review.csv文件，将数据写入reviewResult.csv文件
    with open(filepath1, 'r', encoding='utf-8') as f1:
        reader1 = csv.reader(f1)
        result = list(reader1)
    with open(filepath2, 'r', encoding='utf-8') as f2:
        reader2 = csv.reader(f2)
        review = list(reader2)
    with open('../Data/reviewForInfer/reviewResult.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['review', 'result'])
        for i in range(len(result)):
            writer.writerow([review[i][0], result[i][0]])
    # 将reviewResult.csv文件写入MySQL数据库
    fileName = '../Data/reviewForInfer/reviewResult.csv'
    writeInMySQL(fileName, tablename5)
