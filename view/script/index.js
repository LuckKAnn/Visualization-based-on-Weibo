var myChart = echarts.init(document.getElementById('main'),'customed');
// 指定图表的配置项和数据
option = {
    title: {
        text: '每日话题热度分配',
     },
    tooltip: {
        trigger: 'axis',
        formatter(params){
            var res='<div><p>时间：'+params[0].name+'</p></div>' 
            for(var i=0;i<params.length;i++){
                if (i!=1){
                    res+='<p>'+params[i].marker+params[i].seriesName+'：'+params[i].data+'</p>'
                }
            }
            return res;

        }
    },
    legend: {
        data: ['话题比例','政治话题', '疫情话题','文化娱乐话题','社会新闻话题','其他话题','全国累计确诊人数'],
        right: 0
    },
    grid: {
        left: '3%',
        right: '3%',
        bottom: '3%',
        containLabel: true
    },

    dataZoom:[
        {
        type:"inside",         //缩放
        minValueSpan: 30,
        }
    ],

    xAxis: [
        {
            type: 'category',
            data: function () {
                        var list = [];
                        for (var i = 1; i <= 31; i++) {
                            list.push('12月' + i + '日');
                        }
                        for (var i = 1; i <= 31; i++) {
                            list.push('1月' + i + '日');
                        }
                        for (var i = 1; i <= 29; i++) {
                            list.push('2月' + i + '日');
                        }
                        for (var i = 1; i <= 31; i++) {
                            list.push('3月' + i + '日');
                        }
                        for (var i = 1; i <= 10; i++) {
                            list.push('4月' + i + '日');
                        }
                        return list;
                    }()
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '全国累计确诊人数'
        },
        {
            type: 'value',
            min: 0,
            max: 3.5,
            show: false,
        }
    ],
    series: [
        {
            name: '全国累计确诊人数',
            type: 'line',
            data:[]
        },
        {
            name: '话题比例',
            type: 'bar',
            stack: '话题',
            itemStyle: {
                barBorderColor: 'rgba(0,0,0,0)',
                color: 'rgba(0,0,0,0)'
            },
            emphasis: {
                itemStyle: {
                    barBorderColor: 'rgba(0,0,0,0)',
                    color: 'rgba(0,0,0,0)'
                }
            },
            data: []
        },
        {
            name: '政治话题',
            type: 'bar',
            stack: '话题',
            yAxisIndex: 1,
            data: []
        },
        {
            name: '疫情话题',
            type: 'bar',
            stack: '话题',
            yAxisIndex: 1,
            data: []
        },
        {
            name: '文化娱乐话题',
            type: 'bar',
            stack: '话题',
            yAxisIndex: 1,
            data: []
        },
        {
            name: '社会新闻话题',
            type: 'bar',
            stack: '话题',
            yAxisIndex: 1,
            data: []
        },
        {
            name: '其他话题',
            type: 'bar',
            stack: '话题',
            yAxisIndex: 1,
            data: []
        }
    ]
};

$.get('http://101.200.87.37/main.json').done(function (data) {
    // 填入数据
    myChart.setOption({     
        series: [
            {
                name: '全国累计确诊人数',
                data: data.data1
            },
            {
                name: '话题比例',
                data: data.data1
            },
            {
                name: '政治话题',
                data: data.data2
            },
            {
                name: '疫情话题',
                data: data.data3
            },
            {
                name: '文化娱乐话题',
                data: data.data4
            },
            {
                name: '社会新闻话题',
                data: data.data5
            },
            {
                name: '其他话题',
                data: data.data6
            }
        ]
    });
});
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
//鼠标点击事件
myChart.on('click', function (params) {
    document.getElementById("txt").innerHTML=params.name+"疫情舆论";
    drawAgeAndSex(params.dataIndex);
	drawInfor(params.dataIndex);
    drawwords(params.dataIndex); 
    drawweek1(parseInt(params.dataIndex/7))  
    drawradarchart(params.dataIndex);   
});
drawwords(51); 
drawweek1(7);  
drawradarchart(51); 

 
//**************************************************************************************************雷达图函数*/
function drawradarchart(i){

var myChart = echarts.init(document.getElementById('radarchart'),'customed');
// 指定图表的配置项和数据

option = {
    title: {
        text: '最热话题雷达图'
    },
    tooltip: {},
    legend: {
        data: ['正面言论', '负面言论'],
        right:10
    },
    radar: {
        // shape: 'circle',
        name: {
            textStyle: {
                color: '#fff',
                backgroundColor: '#999',
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        indicator: [
        ]
    },
    series: [{
        name: '正面言论 vs 负面言论',
        type: 'radar',
        // areaStyle: {normal: {}},
        data: [
            {
                value: [],
                name: '负面言论'
            },
            {
                value: [],
                name: '正面言论'
            }
        ]
    }]
};

$.get('http://101.200.87.37/radarchart.json').done(function (data) {
    // 填入数据
    myChart.setOption({  
        radar: {
            // shape: 'circle',
            indicator: [
                { name: data.date[i].name[0], max: 1},
                { name: data.date[i].name[1], max: 1},
                { name: data.date[i].name[2], max: 1},
                { name: data.date[i].name[3], max: 1},
                { name: data.date[i].name[4], max: 1},
                { name: data.date[i].name[5], max: 1}
            ]
        },   
        series: [
            {
                name: '正面言论 vs 负面言论',
                data: [
                    {
                        value: data.date[i].value2,
                        name: '负面言论'
                    },
                    {
                        value: data.date[i].value1,
                        name: '正面言论'
                    }
                ]
            }        
        ]
    });
});

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
}



//****************************************************************************词云***********************/
function drawwords(i){
        var myChart = echarts.init(document.getElementById('words'),'customed');
        //image 选取有严格要求不可过大；，否则firefox不兼容  iconfont上面的图标可以
            option={
                tooltip: {
                    show: true
                },
                series: [{
                    type: 'wordCloud',
                    gridSize: 1,
                    sizeRange: [10,90],
                    rotationRange: [-45, 0, 45, 90],
                    shape: 'circle',

                    textStyle: {
                        normal: {
                            //随机生成颜色
                            color: function () {
                                return 'rgb(' +
                                    Math.round(Math.random() * 255) +
                                    ', ' + Math.round(Math.random() * 255) +
                                    ', ' + Math.round(Math.random() * 255) + ')'
                            }
                        }
                    },
                    left: 'center',
                    top: 'center',
                    // width: '96%',
                    // height: '100%',
                    right: null,
                    bottom: null,
                    // width: 300,
                    // height: 200,
                    // top: 20,
                    data: []
                }]
            }
            $.get('http://101.200.87.37/word.json').done(function (data) {
                // 填入数据
                myChart.setOption({     
                    series: [
                        {
                            data:  data.date[i]                            
                        }        
                    ]
                });
            });
            myChart.setOption(option);
       

}

//*****************************************************************************************周话题 ****************************************/
function drawweek1(i){
    var myChart = echarts.init(document.getElementById('week1'),'customed');
    // 指定图表的配置项和数据
    option = {
        title: {
            text: '周话题热榜',
            left: 0,
            top:36,
            textStyle:{
                fontSize:18
            }
         },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'none'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            containLabel: true,
            left: 0,
            right: '3%',
            bottom: '3%',
        },
        xAxis: {
            name: '热度指数',
            show: false,
    },
        yAxis: {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLabel:{
                show: false
            },
            data:[]
        },
      
        series: [
            {
                type: 'bar',
                 itemStyle: { 
                     normal: {  
                         color: function(params) {   
                             var colorList = ['#96dee8','#6be6c1','#a0a7e6','#626c91'];
                             
                             return colorList[params.dataIndex]
                        }
                     }
                 },
            
                 data:[]
            }
        ]
    };
    
    $.get('http://101.200.87.37/week.json').done(function (data) {
                    // 填入数据
                    myChart.setOption({ 
                        yAxis:[{
                            data:data.week[i].name
                        }],    
                        series: [
                            {
                                data:data.week[i].value                           
                            }        
                        ]
                    });
                });
                myChart.setOption(option);
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    drawweek2(i+1)
    drawweek3(i+2)
    drawweek4(i+3)
    
}
//******************************* */
function drawweek2(i){
    var myChart = echarts.init(document.getElementById('week2'),'customed');
    // 指定图表的配置项和数据
    option = {
        title: {
            text: '  ',
            left: 0,
            top:36,
            textStyle:{
                fontSize:18
            }
         },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'none'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            containLabel: true,
            left: 0,
            right: '3%',
            bottom: '3%',
        },
        xAxis: {
            name: '热度指数',
            show: false,
    },
        yAxis: {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLabel:{
                show: false
            },
            data:[]
        },
      
        series: [
            {
                type: 'bar',
                 itemStyle: { 
                     normal: {  
                         color: function(params) {   
                            //  var colorList = ['#91c7ae','#d48265','#2f4554','#c23531'];
                            var colorList = ['#96dee8','#6be6c1','#a0a7e6','#626c91'];
                             return colorList[params.dataIndex]
                        }
                     }
                 },
            
                 data:[]
            }
        ]
    };
    
    $.get('http://101.200.87.37/week.json').done(function (data) {
                    // 填入数据
                    myChart.setOption({ 
                        yAxis:[{
                            data:data.week[i].name
                        }],    
                        series: [
                            {
                                data:data.week[i].value                           
                            }        
                        ]
                    });
                });
                myChart.setOption(option);
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    
}

function drawweek3(i){
    var myChart = echarts.init(document.getElementById('week3'),'customed');
    // 指定图表的配置项和数据
    option = {
        title: {
            text: '  ',
            left: 0,
            top:36,
            textStyle:{
                fontSize:18
            }
         },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'none'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            containLabel: true,
            left: 0,
            right: '3%',
            bottom: '3%',
        },
        xAxis: {
            name: '热度指数',
            show: false,
    },
        yAxis: {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLabel:{
                show: false
            },
            data:[]
        },
      
        series: [
            {
                type: 'bar',
                 itemStyle: { 
                     normal: {  
                         color: function(params) {   
                            //  var colorList = ['#91c7ae','#d48265','#2f4554','#c23531'];
                            var colorList = ['#96dee8','#6be6c1','#a0a7e6','#626c91'];
                             return colorList[params.dataIndex]
                        }
                     }
                 },
            
                 data:[]
            }
        ]
    };
    
    $.get('http://101.200.87.37/week.json').done(function (data) {
                    // 填入数据
                    myChart.setOption({ 
                        yAxis:[{
                            data:data.week[i].name
                        }],    
                        series: [
                            {
                                data:data.week[i].value                           
                            }        
                        ]
                    });
                });
                myChart.setOption(option);
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    
}

function drawweek4(i){
    var myChart = echarts.init(document.getElementById('week4'),'customed');
    // 指定图表的配置项和数据
    option = {
        title: {
            text: '  ',
            left: 0,
            top:36,
            textStyle:{
                fontSize:18
            }
         },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'none'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            containLabel: true,
            left: 0,
            right: '3%',
            bottom: '3%',
        },
        xAxis: {
            name: '热度指数',
            show: false,
    },
        yAxis: {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLabel:{
                show: false
            },
            data:[]
        },
      
        series: [
            {
                type: 'bar',
                 itemStyle: { 
                     normal: {  
                         color: function(params) {   
                            //  var colorList = ['#91c7ae','#d48265','#2f4554','#c23531'];
                            var colorList = ['#96dee8','#6be6c1','#a0a7e6','#626c91'];
                             return colorList[params.dataIndex]
                        }
                     }
                 },
            
                 data:[]
            }
        ]
    };
    
    $.get('http://101.200.87.37/week.json').done(function (data) {
                    // 填入数据
                    myChart.setOption({ 
                        yAxis:[{
                            data:data.week[i].name
                        }],    
                        series: [
                            {
                                data:data.week[i].value                           
                            }        
                        ]
                    });
                });
                myChart.setOption(option);
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    
}
//************************************************************************************************************* */