var column = echarts.init(document.getElementById('column'));

var columnOption = {
    title: [
      {
        text: 'Video Statistics',
        left: 'left',
        subtext: ' V: View\n B: Barrage\n R: Review\n F: Favorite\n C: Coin\n S: Share\n L: Like',
      }
    ],
    polar: {
      radius: [30, '80%']
    },
    radiusAxis: {
      max: 1000,
    },
    angleAxis: {
      type: 'category',
      data: ['a', 'b', 'c', 'd'],
      startAngle: 75
    },
    tooltip: {},
    series: {
      type: 'bar',
      data: [2, 1.2, 2.4, 3.6],
      coordinateSystem: 'polar',
      label: {
        show: true,
        position: 'middle',
        formatter: '{b}: {c}'
      }
    },
    animation: false
  };
column.setOption(columnOption);