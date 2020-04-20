//树形图
// $(document).ready(function(){

    
//创建echarts对象在container容器中
var dom = document.getElementById("container");

var myChart = echarts.init(dom);
console.log("mychart"+myChart);
var originTrainPlain = null;


var app = {};
var option = null;
 
// --------------------------------------------------------------//
/*
函数(1) clickFun:
    功能: 点击计划树叶子节点时(即课程节点)改变其状态。
    状态:
        绿色: 已选课
        黄色: 预选课
        红色：未选课
    状态变化
        红->黄->绿->红
 */
myChart.on("click", clickFun);
//点击变色
function clickFun(param) {
 
    if (typeof param.seriesIndex == 'undefined') {
        return;
    }
    //只有最后一个参数可以点击
    if (param.type == 'click' && typeof param.data.children == "undefined") {
        console.log(param.data.name);
        if (param.data.itemStyle.borderColor == 'red') {
            param.data.itemStyle.borderColor = 'yellow';
            param.data.itemStyle.Color = 'yellow';
        }
        else if(param.data.itemStyle.borderColor == 'yellow') {
            param.data.itemStyle.borderColor = 'red';
            param.data.itemStyle.Color = 'red';
        }
        // else{
            // param.data.itemStyle.borderColor = 'red';
            // param.data.itemStyle.Color = 'red';
        // }
        myChart.setOption({});
        // console.log(myChart);
        // console.log(param.data.itemStyle.borderColor);
    }
};

// --------------------------------------------------------------//


//--------------------------------------------------------------//
/*
函数(2)$.getJson('/get_info', function(data){...}
    功能： 绑定路由"get_info", 从数据库中获得数据，初始化计划树
 */
myChart.showLoading();
$.getJSON('/get_info', function(data)
{
    // console.log(2222)
    myChart.hideLoading();
    // alert("getjson 函数");
   
    originTrainPlain = data;
    console.log(data);
    console.log(new Date().getTime())
    option = {
        // 配置提示信息
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        // 图标类型
        series:[
            {
                type: 'tree',
              
                data: [data],
    
                left: '2%',
                right: '2%',
                top: '8%',
                bottom: '20%',
                // 图元的图形类别
                symbol: 'emptyCircle',
                //图元的大小
                symbolSize: 7,

                orient: 'vertical',
                // 控制显示层数
                initialTreeDepth: 4,
                expandAndCollapse: true,
                // 高亮时显示的内容设置
                label: {
                    normal: {
                        position: 'bottom',
                        rotate: -90,
                        verticalAlign: 'middle',
                        align: 'left',
                        fontSize: 9
                    }
                },
    
                leaves: {
                     // 高亮时显示的内容设置
                    label: {
                        normal: {
                            position: 'bottom',
                            rotate: -90,
                            verticalAlign: 'middle',
                            align: 'left'
                        }
                    },
                    //设置图表标志的大小
                    symbolSize: 15
                },
                //数据更新动画的时长
                animationDurationUpdate: 750
            }
        ]};
    
    
    myChart.setOption(option);
    // console.log("mychart 的值2"+myChart);
    // console.log("mychart option的值1"+myChart.getOption().series[0].data);

});


//----------------------------------------------------------------//



// ------------------------------------------------------------------//
/*
函数(3) getScore()
    功能: 使用深度优先搜索，计算每一类课程已修学分(绿色)和预选学分(黄色)
          结果分别存储到perExistScore和perAddScore中。
          以供实现计划树和进度条的同步.
 */
//已修学分
var perExistScore=0;
//预加学分
var perAddScore=0;
console.log("peraddscore 的值是： "+perAddScore);
function getScore(Node){
    if(typeof Node.children == 'undefined'){
        if(Node.itemStyle.borderColor == "yellow"){
            perAddScore += Node.value;
        }
        else if (Node.itemStyle.borderColor == "green"){
            perExistScore += Node.value;
            
        }
    }
    else{
        // console.log(Node["children"]);
        for (var sub = 0; sub < Node["children"].length; sub++)
            getScore(Node["children"][sub]);
    }
}
//  function getColor(Node){
    
//     if(typeof Node.children == 'undefined'){
//         if(Node.itemStyle.borderColor == "yellow"){
//             perAddScore += Node.value;
//         }
//         else if (Node.itemStyle.borderColor == "green"){
//             perExistScore += Node.value;
        
            
//         }
//     }
//     else{
//         // console.log(Node["children"]);
//         for (var sub = 0; sub < Node["children"].length; sub++)
//             {getScore(Node["children"][sub]);
//             console.log(Node['children'][sub]);   
//         }
//     }
    
//  }

    
//------------------------------------------------------------------------//
// var option = myChart.getOption();
// console.log(option,'option')
// console.log(new Date().getTIme())
// -----------------------------------------------------------------------//
/*
函数(4):setInterval(function(){...}
    功能: 定时根据计划树更新进度条进度。若所修学分超过所需学分，则进度条不再更新变化。
 */

function fuckThisBug (){
    console.log("fuck 函数");
    //得到传入的树形图一摸一样的数据
  
   var Tree = myChart.getOption()["series"][0]["data"][0];
   console.log(Tree);

   var subjects = ["专业实践必修", "专业理论必修", "专业理论选修", "学科实践必修", "学科理论必修", "实践选修", "第三课堂", "通识实践必修", "通识理论必修",
     "通识理论选修(公选)"];
  
   var subjects2TotalScore = {};  //所需总学分。每科分开
   var subjects2ExistScore = {};  //已修学分(绿色)每科分开
   var subjects2AddScore = {};  //拟增加学分(黄色)每科分开
   // 初始化已选分数和总分数
   for(var i=0; i<subjects.length;i++){
       subjects2TotalScore[subjects[i]] = Tree.children[i].value;
    //    console.log("总分数parent"+Tree.children[i].value);
    //    console.log(subjects[i]+"总分数"+subjects2TotalScore[subjects[i]]);
       subjects2ExistScore[subjects[i]] = 0;
       subjects2AddScore[subjects[i]] = 0;
       // console.log(subjects2TotalScore+"111");
       // console.log(subjects2ExistScore+"222");
       // console.log(subjects2AddScore+"333");
   }
   // 求得每科已选的学分和（绿） 将选分数和（黄色）
   for(var sub =0; sub <subjects.length; sub++){
       perExistScore = 0;
       perAddScore = 0;
//调用函数,获得 perAddScore  perExistScore的值
       getScore(Tree['children'][sub]);
       subjects2ExistScore[subjects[sub]] = perExistScore;
       subjects2AddScore[subjects[sub]] = perAddScore;
   }
 


   var TotalScore = 0; //total记录的是所有需要的学分
   var TotalExistScore = 0;//绿色
   var TotalAddScore = 0;//黄色

   for(var i=0; i<subjects.length; i++){
       TotalScore += subjects2TotalScore[subjects[i]];//所有科目总分数
    //    console.log(subjects[i]+"总分数"+TotalScore);
       TotalExistScore += Math.min(subjects2ExistScore[subjects[i]],subjects2TotalScore[subjects[i]]);
       if(subjects2TotalScore[subjects[i]] - subjects2ExistScore[subjects[i]] > 0)
           TotalAddScore += Math.min(subjects2TotalScore[subjects[i]]-subjects2ExistScore[subjects[i]], subjects2AddScore[subjects[i]]);

   }

   
    
   // 生成进度条标签
   var processes = [];
   var pLabels = [];
   //更新除总进度条外的进度条
   for(var i=2; i< subjects.length+2; i++){
       processes.push("process-parent"+i.toString());//每一个进度条黄+绿总进度
       pLabels.push("on" + i.toString());//绿
   }
   // 更新总进度条
   var greenWidth, yellowWidth;

   var doms = document.getElementsByClassName("process-parent1")[0].children;
   greenWidth = (TotalExistScore*100/TotalScore).toFixed(2);//四舍五入为指定小数位数
   greenWidth =  Math.min(100, greenWidth);
   yellowWidth = (TotalAddScore*100/TotalScore).toFixed(2);
   yellowWidth = Math.min(100-greenWidth, yellowWidth)
   doms[0].style.width = greenWidth + "%";
   doms[1].style.width = yellowWidth + "%";
   dom = document.getElementById("on1");
   dom.textContent = TotalExistScore + '/' + TotalScore;

   // 设置各个子进度条

   for(var idx=0; idx<processes.length; idx++){
       TotalScore = subjects2TotalScore[subjects[idx]];
       TotalExistScore = subjects2ExistScore[subjects[idx]];
       TotalAddScore = subjects2AddScore[subjects[idx]];
       var doms = document.getElementsByClassName(processes[idx])[0].children;
       greenWidth = (TotalExistScore*100/TotalScore).toFixed(2);
       greenWidth =  Math.min(100, greenWidth);
       yellowWidth = (TotalAddScore*100/TotalScore).toFixed(2);
       yellowWidth = Math.min(100-greenWidth, yellowWidth)
       doms[0].style.width = greenWidth + "%";
       doms[1].style.width = yellowWidth + "%";
       dom = document.getElementById(pLabels[idx]);
       dom.textContent = TotalExistScore + '/' + TotalScore;
   }



//    for(var i=2; i< subjects.length+2; i++){
//     if(progress[i].length!=0)

// }
}

 
window.onload=function(){
    
  
setInterval(function(){fuckThisBug();}, 2000);}
// domain.onchange=changeDomain;




//-----------------------------------------------------------------------//
// 