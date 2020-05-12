var domCourse = document.getElementById("course_box");
var domPerson = document.getElementById("person_box");
var domIntersting = document.getElementById("intersting_box");
var domAcknowledge = document.getElementById("acknowledge_box");
var chartCourse = echarts.init(domCourse);
var chartPerson = echarts.init(domPerson);
var chartIntersting = echarts.init(domIntersting);
var chartAcknowledge = echarts.init(domAcknowledge);
var app = {};
var optionCourse = null;
var optionPerson = null;
var  optionIntersting =null;
var  optionAcknowledge =null;


$.getJSON('/getRecommedData', function(coursePersonJson)
{
    // console.log(3333)
    var optionCourse = {
        dataset: coursePersonJson['course'],
        grid: {containLabel: true},
        xAxis: {name: '喜爱程度'},
        yAxis: {type: 'category'},
        visualMap: {
            orient: 'horizontal',
            left: 'center',
            min: 1,
            max: 5,
            text: ['High Score', 'Low Score'],
            // Map the score column to color
            dimension: 0,
            inRange: {
                color: ['#D7DA8B', '#E15457']
            }
        },
        series: [
            {
                type: 'bar',
                encode: {
                    // Map the "amount" column to X axis.
                    x: 'amount',
                    // Map the "product" column to Y axis
                    y: 'product'
                }
            }
        ]
    };
    var optionPerson = {
        dataset: coursePersonJson['passCourse'],
        grid: {containLabel: true},
        xAxis: {name: '相似度'},
        yAxis: {type: 'category'},
        visualMap: {
            orient: 'horizontal',
            left: 'center',
            min: 0.7,
            max: 1,
            text: ['High Score', 'Low Score'],
            // Map the score column to color
            dimension: 0,
            inRange: {
                color: ['#D7DA8B', '#E15457']
            }
        },
        series: [
            {
                type: 'bar',
                encode: {
                    // Map the "amount" column to X axis.
                    x: 'amount',
                    // Map the "product" column to Y axis
                    y: 'product'
                }
            }
        ]
    };
     var optionIntersting= {
        dataset: coursePersonJson['interstingCourse'],
        grid: {containLabel: true},
        xAxis: {name: '相似度'},
        yAxis: {type: 'category'},
        visualMap: {
            orient: 'horizontal',
            left: 'center',
            min: 0.7,
            max: 1,
            text: ['High Score', 'Low Score'],
            // Map the score column to color
            dimension: 0,
            inRange: {
                color: ['#D7DA8B', '#E15457']
            }
        },
        series: [
            {
                type: 'bar',
                encode: {
                    // Map the "amount" column to X axis.
                    x: 'amount',
                    // Map the "product" column to Y axis
                    y: 'product'
                }
            }
        ]
    };
     var optionAcknowledge = {
        dataset: coursePersonJson['acknowledgeCourse'],
        grid: {containLabel: true},
        xAxis: {name: '相似度'},
        yAxis: {type: 'category'},
        visualMap: {
            orient: 'horizontal',
            left: 'center',
            min: 0.7,
            max: 1,
            text: ['High Score', 'Low Score'],
            // Map the score column to color
            dimension: 0,
            inRange: {
                color: ['#D7DA8B', '#E15457']
            }
        },
        series: [
            {
                type: 'bar',
                encode: {
                    // Map the "amount" column to X axis.
                    x: 'amount',
                    // Map the "product" column to Y axis
                    y: 'product'
                }
            }
        ]
    };
    if (optionCourse && typeof optionCourse === "object") {
        // console.log(optionCourse)
        chartCourse.setOption(optionCourse, true);
        // console.log(chartCourse)
    }
    if (optionPerson && typeof optionPerson === "object") {
        // console.log(optionPerson)
        chartPerson.setOption(optionPerson, true);
        // console.log(chartPerson)
    }
    if (optionIntersting && typeof optionIntersting === "object") {
        // console.log(optionPerson)
        chartIntersting.setOption(optionIntersting, true);
        // console.log(chartPerson)
    }
    if (optionAcknowledge && typeof optionAcknowledge === "object") {
         console.log(optionAcknowledge)
        chartAcknowledge.setOption(optionAcknowledge, true);
        // console.log(chartPerson)
    }
});
