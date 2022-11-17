$('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});


function initColumn() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        y: ['视频1', '视频2', '视频3', '视频4', '视频5', '视频6', '视频7', '视频8', '视频9'],
        ColumnData: [1, 2, 3, 4, 5, 6, 7, 8, 10]
    }

    $.ajax({
        async: false,
        url: "/getColumnData",
        timeout: 3000,
        success: function (data) {
            // console.log("This is ajax data: ", data);
            newY = [];
            newColumnData = [];
            // console.log("This is data.sumGrade: ", data.sumGrade);
            //将data.sumGrade的值赋值给newColumnData
            for (var i = 0; i < data.sumGrade.length; i++) {
                //将sumGrade转换为整数
                newColumnData.push(parseInt(data.sumGrade[i]));
            }
            //将data.title的值赋值给newY
            for (var i = 0; i < data.title.length; i++) {
                //将title的前三个字符赋值给newY
                newY.push(data.title[i].substring(0, 7));
            }
            // console.log("This is newColumnData: ", newColumnData);
            // console.log("This is newY: ", newY);
            dataset.y = newY;
            dataset.ColumnData = newColumnData;
        },
        error: function (data) {
            console.log(data);
        }
    });

    // console.log("This is dataset: ",dataset);
    var chart1 = $("#container1").highcharts({
        chart: {
            renderTo: 'container1', //装载图表的div容器id
            type: 'bar',
            backgroundColor: '#1e2131',
            plotBorderColor: '#1c2a38',
            plotBorderWidth: 1,
        },
        title: false,//主标题
        subtitle: false,//副标题
        exporting: {
            enabled: false, //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        xAxis: {
            // categories: ['视频1','视频2','视频3','视频4','视频5','视频6','视频7','视频8','视频9'],
            categories: dataset.y,
            labels: {
                style: {
                    color: '#9ea0ae'
                }
            },
            tickWidth: '0',
            tickColor: '#1c2a38',
            lineColor: '#1c2a38',
        }, // x系列设置
        yAxis: {
            // min: 0,
            title: {
                text: '分数',
                align: 'high'
            },
            tickColor: '#1c2a38',
            gridLineColor: '#1c2a38',
            labels: {
                overflow: 'justify'
            }
        },// y系列设置
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true,
                    allowOverlap: true,
                    color: '#fff',
                },
                borderColor: "",//去边框
                color: '#0084fe'
            }
        },
        legend: false,
        credits: {
            enabled: false
        },
        series: [{
            name: '综合评分',
            // data: [635,400,300, 203,107,100,65,38,31],
            data: dataset.ColumnData,
            color: '#0084fe',
            border: '#0084fe'
        }]
    });
};

function initBar() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        categories: ['0-1min', '1-5min', '5-10min', '10-30min', '30-60min', '>60min'],
        data1: [5, 0, 0, 0, 0, 0],
        data2: [0, 78, 0, 0, 0, 0],
        data3: [0, 0, 55, 0, 0, 0],
        data4: [0, 0, 0, 10, 0, 0],
        data5: [0, 0, 0, 0, 20, 0],
        data6: [0, 0, 0, 0, 0, 8],
    }

    $.ajax({
        async: false,
        url: "/getBarData",
        timeout: 3000,
        success: function (data) {
            // console.log("This is getBardata: ", data);
            // console.log("This is data.timelength[0]: ", data.timelength[0]);
            // console.log("This is length: ", data.timelength.length);
            //类比0-60s, 60-300s, 300-600s, 600-1800s, 1800-3600s, >3600s
            var time0_60 = 0;
            var time60_300 = 0;
            var time300_600 = 0;
            var time600_1800 = 0;
            var time1800_3600 = 0;
            var time3600 = 0;
            for (var i = 0; i < data.timelength.length; i++) {
                if (data.timelength[i] <= 60) {
                    time0_60++;
                } else if (data.timelength[i] > 60 && data.timelength[i] <= 300) {
                    time60_300++;
                } else if (data.timelength[i] > 300 && data.timelength[i] <= 600) {
                    time300_600++;
                } else if (data.timelength[i] > 600 && data.timelength[i] <= 1800) {
                    time600_1800++;
                } else if (data.timelength[i] > 1800 && data.timelength[i] <= 3600) {
                    time1800_3600++;
                } else if (data.timelength[i] > 3600) {
                    time3600++;
                }
            }
            dataset.data1[0] = time0_60;
            dataset.data2[1] = time60_300;
            dataset.data3[2] = time300_600;
            dataset.data4[3] = time600_1800;
            dataset.data5[4] = time1800_3600;
            dataset.data6[5] = time3600;
        },
        error: function (data) {
            console.log(data);
        }
    });

    // console.log("This is dataset: ",dataset);
    var chart3 = $("#jglxchart").highcharts({
        chart: {
            backgroundColor: '#1e2131',
            type: 'column',
            plotBorderColor: '#1c2a38',
            plotBorderWidth: 1,
        },
        title: false,
        xAxis: {
            gridLineColor: '#1c2a38',//网格线
            tickColor: '#1c2a38',//刻度线
            lineColor: '#1c2a38',//轴线
            // categories: ['宏观经济', '资本市场', '货币市场', '外汇市场', '债券市场','大宗商品']
            categories: dataset.categories
        },
        yAxis: {
            min: 0,
            title: false,
            gridLineColor: '#1c2a38',//网格线
            tickColor: '#1c2a38',//刻度线
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || '#fff'
                }//柱形图上方数据显示
            }
        },
        exporting: {
            enabled: false, //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        credits: {
            enabled: false // 禁用版权信息
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            itemStyle: { cursor: 'pointer', color: '#FFF' },
            itemHiddenStyle: { color: '#CCC' },
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '<br/>' +
                    '总量: ' + this.point.stackTotal;
            }
        },
        plotOptions: {
            column: {           //不显示阴影
                stacking: 'normal',
                bar: false,
                borderWidth: 0,  //柱子边框的大小
            },
        },
        series: [{
            name: '0-1min',
            // data: [5, 0, 0]
            data: dataset.data1
        }, {
            name: '1-5min',
            // data: [0, 2, 0]
            data: dataset.data2
        },
        {
            name: '5-10min',
            // data: [0, 0, 4]
            data: dataset.data3
        },
        {
            name: '10-30min',
            // data: [0, 0, 4]
            data: dataset.data4
        },
        {
            name: '30-60min',
            // data: [0, 0, 4]
            data: dataset.data5
        },
        {
            name: '>60min',
            // data: [0, 0, 4]
            data: dataset.data6
        }
        ]

    });
};

function initLine() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        categories: ['原创', '转载', '合作'],
        data1: [5, 0, 0],
        data2: [0, 2, 0],
        data3: [0, 0, 4],
    }

    //    $.ajax({
    //        async: false,
    //        url: "/getColumnData",
    //        timeout: 3000,
    //        success: function (data) {
    //            // console.log("This is ajax data: ",data);
    //            Cdata = [];
    //            //将data.viedo1-9的值赋值给Cdata
    //            Cdata.push(data.viedo1[1]);
    //            Cdata.push(data.viedo2[1]);
    //            Cdata.push(data.viedo3[1]);
    //            // dataset.data1[0] = Cdata[0];
    //            // dataset.data2[1] = Cdata[1];
    //            // dataset.data3[2] = Cdata[2];
    //        },
    //        error: function (data) {
    //            console.log(data);
    //        }
    //    });

    // console.log("This is dataset: ",dataset);
    var chart4 = $("#qst-monthchart").highcharts({
        chart: {
            backgroundColor: '#1e2131',
            plotBorderColor: '#1c2a38',
            plotBorderWidth: 1
        },
        title: {
            text: false,
        },
        credits: {
            enabled: false // 禁用版权信息
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tickColor: '#1c2a38',
            gridLineColor: '#1c2a38',
            lineColor: '#1c2a38',
        },
        yAxis: {
            title: false,
            gridLineColor: '#1c2a38',
            tickColor: '#1c2a38'
        },
        tooltip: {
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            itemStyle: { cursor: 'pointer', color: '#FFF' },
            itemHiddenStyle: { color: '#CCC' },
        },
        series: [{
            name: '暂无数据',
            data: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 16, 12]
        }, {
            name: '暂无数据',
            data: [3, 5, 7, 9, 11, 13, 15, 17, 19, 18, 17, 16]
        }, {
            name: '暂无数据',
            data: [3, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
        }, {
            name: '暂无数据',
            data: [10, 14, 18, 22, 30, 28, 26, 24, 22, 21, 20, 19]
        }, {
            name: '暂无数据',
            data: [6, 8, 10, 13, 15, 16, 18, 19, 18, 17, 16, 15]
        }, {
            name: '暂无数据',
            data: [8, 10, 12, 14, 16, 18, 16, 14, 13, 12, 11, 10],
        }]
    });
};

function initCircle() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        name1: '消极',
        name2: '积极',
        y1: 70,//为了显示效果，这里的值是百分比
        y2: 30,
    }

       $.ajax({
           async: false,
           url: "/getCircleData",
           timeout: 3000,
           success: function (data) {
            //    console.log("This is circle data: ",data);
                // 将data.count1-2的值转为百分比
                temp0=parseInt(data.count0);
                temp1=parseInt(data.count1);
                var sum=temp0+temp1;
                var y1=parseInt((temp0/sum)*100);
                var y2=parseInt((temp1/sum)*100);
                dataset.y1=y1;
                dataset.y2=y2;
           },
           error: function (data) {
               console.log(data);
           }
       });

    var chart6 = $("#rj-daychart").highcharts({
        chart: {
            backgroundColor: '#1e2131',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            spacing: [20, 0, 20, 0]
        },
        title: false,
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        exporting: {
            enabled: false, //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        credits: {
            enabled: false // 禁用版权信息
        },
        plotOptions: {
            pie: {
                borderWidth: 0,
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    color: '#fff',
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            innerSize: '80%',
            name: '评论数量',
            data: [
                {
                    // name: '人工',
                    // y: 40
                    name: dataset.name1,
                    y: dataset.y1
                },
                {
                    // name: '机器人',
                    // y: 60,
                    name: dataset.name2,
                    y: dataset.y2,
                    sliced: true,
                    selected: true,
                }
            ]
        }]
    });
};

function initPie() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        y1: 40,
        y2: 60,
        y3: 20,
        y4: 80,
        y5: 30,
        y6: 70,
        y7: 10,
    }

    $.ajax({
        async: false,
        url: "/getPieData",
        timeout: 3000,
        success: function (data) {
            // console.log("This is pie data: ",data);
            dataset.y1=parseInt(data.viewSum);
            dataset.y1=parseInt(data.viewSum);
            dataset.y2=parseInt(data.barrageSum);
            dataset.y3=parseInt(data.replySum);
            dataset.y4=parseInt(data.favoriteSum);
            dataset.y5=parseInt(data.coinSum);
            dataset.y6=parseInt(data.shareSum);
            dataset.y7=parseInt(data.likeSum);
        },
        error: function (data) {
            console.log(data);
        }
    });

    var chart8 = $("#fbt-monthchart").highcharts({
        chart: {
            backgroundColor: '#1e2131',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: false,
        tooltip: {
            headerFormat: '{series.name}<br>',
            pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
        },
        exporting: {
            enabled: false, //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        credits: {
            enabled: false // 禁用版权信息
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            itemStyle: { cursor: 'pointer', color: '#FFF' },
            itemHiddenStyle: { color: '#CCC' },
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || '#FFF'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: '各信息占比',
            data: [
                {
                    name: '播放',
                    // y: 10,
                    y: dataset.y1,
                    // sliced: true,
                    // selected: true
                },
                // ['宏观经济', 15.0],
                // ['货币市场', 20.0],
                // ['外汇市场', 15.0],
                // ['债券市场', 5.0],
                // ['大宗商品', 35.0],
                {
                    name: '弹幕',
                    // y: 15.0,
                    y: dataset.y2
                },
                {
                    name: '评论',
                    // y: 20.0,
                    y: dataset.y3
                },
                {
                    name: '收藏',
                    // y: 15.0,
                    y: dataset.y4,
                    selected: true,
                    sliced: true
                },
                {
                    name: '投币',
                    // y: 5.0,
                    y: dataset.y5,
                    // selected: true
                },
                {
                    name: '分享',
                    // y: 35.0,
                    y: dataset.y6
                },
                {
                    name: '点赞',
                    // y: 35.0,
                    y: dataset.y7
                }
            ]
        }]
    });
};

function initBox() {
    Highcharts.setOptions({
        colors: ['#8129dd', '#8ec63f', '#2756ca', '#f1b601', '#f86423', '#27aae3']
    });

    dataset = {
        categories: ['宏观经济', '资本市场', '货币市场', '外汇市场', '债券市场', '大宗商品'],
        name: ['播放', '弹幕', '评论', '收藏', '投币', '分享'],
        data1: [15, 3, 24, 7, 2, 4],
        data2: [12, 2, 23, 2, 1, 7],
        data3: [13, 4, 24, 2, 5, 3],
        data4: [14, 2, 21, 3, 2, 6],
        data5: [15, 3, 24, 7, 2, 4],
        data6: [12, 2, 23, 2, 1, 7],
    }

    $.ajax({
        async: false,
        url: "/getBoxData",
        timeout: 3000,
        success: function (data) {
            // console.log('This is box data',data.box[0]);
            // 根据data.box的长度，修改dataset中的categories，data1-6
            for (var i = 0; i < data.box.length; i++) {
                temp = data.box[i][7];
                temp = temp.substring(0, 4);
                dataset.categories[i] = temp;
                dataset.data1[i] = parseInt(data.box[i][0]);
                dataset.data2[i] = parseInt(data.box[i][1]);
                dataset.data3[i] = parseInt(data.box[i][2]);
                dataset.data4[i] = parseInt(data.box[i][3]);
                dataset.data5[i] = parseInt(data.box[i][4]);
                dataset.data6[i] = parseInt(data.box[i][5]);
            }
            
        },
        error: function (data) {
            console.log(data);
        }
    });

    // console.log("This is dataset: ",dataset);
    var chart10 = $("#zxlxchart").highcharts({
        chart: {
            backgroundColor: '#1e2131',
            type: 'column',
            plotBorderColor: '#1c2a38',
            plotBorderWidth: 1,
        },
        title: false,
        xAxis: {
            gridLineColor: '#1c2a38',//网格线
            tickColor: '#1c2a38',//刻度线
            lineColor: '#1c2a38',//轴线
            // categories: ['宏观经济', '资本市场', '货币市场', '外汇市场', '债券市场','大宗商品']
            categories: dataset.categories
        },
        yAxis: {
            min: 0,
            title: false,
            gridLineColor: '#1c2a38',//网格线
            tickColor: '#1c2a38',//刻度线
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || '#fff'
                }//柱形图上方数据显示
            }
        },
        exporting: {
            enabled: false, //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        credits: {
            enabled: false // 禁用版权信息
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            itemStyle: { cursor: 'pointer', color: '#FFF' },
            itemHiddenStyle: { color: '#CCC' },
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '<br/>' +
                    '总量: ' + this.point.stackTotal;
            }
        },
        plotOptions: {
            column: {           //不显示阴影
                stacking: 'normal',
                bar: false,
                borderWidth: 0,  //柱子边框的大小
            },
        },
        series: [{
            name: dataset.name[0],
            // data: [15, 3, 24, 7, 2,4]
            data: dataset.data1
        },{
            name: dataset.name[1],
            data: dataset.data2
        },{
            name: dataset.name[2],
            data: dataset.data3
        },{
            name: dataset.name[3],
            data: dataset.data4
        },{
            name: dataset.name[4],
            data: dataset.data5
        },{
            name: dataset.name[5],
            data: dataset.data6
        }]
    });

};

initColumn();
initBar();
// initLine();
initCircle();
initPie();
initBox();
