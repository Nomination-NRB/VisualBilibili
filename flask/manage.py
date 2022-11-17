from flask import render_template
from flask import Flask
from flask import jsonify
import linkSQL

app = Flask(__name__)
getOverViewTable1 = '237733293_overview_data'
getOverViewTable2 = '237733293_video_data'
getColumnTable1 = '237733293_video_data'
getColumnTable2 = '237733293_video_detail_data'
getBarTable = '237733293_video_data'
getFansTable = '237733293_fans_data'
getBoxTable1 = '237733293_video_data'
getBoxTable2 = '237733293_video_detail_data'
getCircleTable = '237733293_reviewresult'
getPieTable = '237733293_video_detail_data'


@app.route('/')
def toIndex():
    return render_template('index.html')


@app.route('/getOverViewData')
def getOverViewData():
    mysum, res = linkSQL.getOverViewData(getOverViewTable1, getOverViewTable2)
    data1 = mysum[0]
    data2 = res[0]
    # following,follower,play_view,article_view
    return jsonify({'following': data1[0], 'follower': data1[1], 'play_view': data1[2], 'article_view': data1[3],
                    'likes': data1[4], 'count': data2[0]})


@app.route('/getColumnData')
def getColumnData():
    mysum = linkSQL.getColumnData(getColumnTable1, getColumnTable2)
    data = mysum
    # title, sumGrade
    # 将data里的title和sumGrade分别放入两个列表中
    title = []
    sumGrade = []
    for item in data:
        title.append(item[0])
        sumGrade.append(item[1])
    return jsonify({'title': title, 'sumGrade': sumGrade})


@app.route('/getBarData')
def getBarData():
    mysum = linkSQL.getBarData(getBarTable)
    data = mysum
    # timelength
    return jsonify({'timelength': data})


@app.route('/getFansData')
def getFansData():
    mysum = linkSQL.getFansData(getFansTable)
    data = mysum
    # fans
    return jsonify({'fans': data})


@app.route('/getBoxData')
def getBoxData():
    mysum = linkSQL.getBoxData(getBoxTable1, getBoxTable2)
    data = mysum
    return jsonify({'box': data})


@app.route('/getCircleData')
def getCircleData():
    count0, count1 = linkSQL.getCircleData(getCircleTable)
    return jsonify({'count0': count0, 'count1': count1})


@ app.route('/getPieData')
def getPieData():
    mysum = linkSQL.getPieData(getPieTable)
    data=mysum[0]
    return jsonify({'viewSum': data[0], 'barrageSum': data[1], 'replySum': data[2], 'favoriteSum': data[3], 'coinSum': data[4], 'shareSum': data[5], 'likeSum': data[6]})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
