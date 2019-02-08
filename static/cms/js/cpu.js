var myChart = echarts.init(document.getElementById('main'));

myChart.setOption({
    title: {},
    tooltip: {},
    legend: {
        data:['cpu']
    },
    xAxis: {
        data: []
    },
    yAxis: {},
    series: [{
        name: 'cpu',
        type: 'line',
        data: []
    }],
    color: ['#00EE00', '#FF9F7F','#FFD700']
});


var time = ["","","","","","","","","",""],
    cpu = [0,0,0,0,0,0,0,0,0,0]


//准备好统一的 callback 函数
var update_mychart = function (res) {
//res是json格式的response对象

    // 隐藏加载动画
    myChart.hideLoading();

    // 准备数据
    time.push(res.data[0]);
    cpu.push(parseFloat(res.data[1]));
    if (time.length >= 10){
        time.shift();
        cpu.shift();
    }

    // 填入数据
    myChart.setOption({
        xAxis: {
            data: time
        },
        series: [{
            name: 'cpu', // 根据名字对应到相应的系列
            data: cpu
        }]
    });

};

// 首次显示加载动画
myChart.showLoading();


// 建立socket连接，等待服务器“推送”数据，用回调函数更新图表
$(document).ready(function() {
    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response', function(res) {
        update_mychart(res);
    });

});