
// -------------------------------------------------//
/*
函数(1):function submit()
    功能:绑定"查询"界面中的“提交”按钮，将用户更新的计划书结果存储到数据库中，并刷新计划书和进度条
 */
var orientation=null;
function submit(){
    alert("提交成功");
    var postData = {};
    var tree = myChart.getOption()['series'][0]['data'][0];
    var scores = course2score;
    var returnData = {'tree':tree, "scores":scores};
    // console.log("提交后返回的数据值"+returnData.scores[0]);
    $.ajax({
        type:'POST',
        url:"submit_train_plan",
        data:JSON.stringify(returnData),  //转化字符串
        // dataType: "json",
        success: function(data){
            // console.log("ajax返回的值"+data);
            console.log("提交的data值"+typeof(data));
            myChart.setOption({
                series:[{
                    name:"trianPlanTree",
                    data: [data]
                }]
            })
            originTrainPlain = data;
        },
        error:function(){
            console.log("错误");
        }
    });
}
//----------------------------------------------------//
/*
函数(2)function rebuild()
    功能：重置计划树和进度条为初始状态(最近一次数据库中状态)
 */
function rebuild(){
    myChart.setOption({
        series:[{
            name:"trianPlanTree",
            data: [originTrainPlain]
        }]
    })
}
// ---------------------------------------------------//

// --------------------------------------------------//
/*
函数(3) function dfsScore()
    功能: 根据计划树和子类别，得到该类别所有课程以及其评分
    输入：Tree, idx（类别)
    返回: {"类别": ["课程一"，"课程二"], [评分1， 评分2]}
 */

var allSujCourse = [];
var allSujScore = [];
var allSujPass=[];
var course2score = {};

function dfsScore(Node){
    if(typeof Node.children == 'undefined' ){
        // console.log(Node.itemStyle.borderColor);
        if(Node.itemStyle.borderColor=="green")
        { 
        allSujCourse.push(Node['name']);
        allSujScore.push(Node['score']);
        allSujPass.push(Node['pass']);
        console.log(allSujPass);
        
   
        //将所有未选课程已经分数对应
        course2score[Node['name']] = {'score':Node['score']};
       
       }
    }
    else{
        // console.log(Node["children"]);
        for (var sub = 0; sub < Node["children"].length; sub++)
            dfsScore(Node["children"][sub]);
    }
}
// -----------------------------------------------------//

// --------------------------------------------------- //
/*
函数(4)：function score()
    功能, 更具计划树初始化评分下拉框，只显示未选课程以及未评分课程
    下拉框1：domain
    下拉框2：course
    下拉框3：score
 */
var allScore = ['1', '2', "3", '4', '5'];
    var courseScore = [];//未选课程的分数
    var courseName = [];//未选课程名称
    var coursePass=[];
    var allSubject = [];
function initScore(){

    console.log("111");
    // console.log(course2score[Node['name']]});
    
   
    // console.log(myChart.getOption());
    Tree = myChart.getOption()['series'][0]['data'][0];
    // Tree=orientation[0];
    for(var idx=0; idx<Tree['children'].length; idx++) {
        var subName = Tree['children'][idx]['name'];
        allSubject.push(subName);
        allSujCourse = [];
        allSujScore = [];
        allSujPass=[];
        //得到未选课程以及未评分的课程
        dfsScore(Tree['children'][idx]);
        
        courseScore.push(allSujScore);
        courseName.push(allSujCourse);
       coursePass.push(allSujPass);
    }
    // console.log("通过与否"+coursePass);
    // console.log(coursePass);
    // console.log("评分的值"+courseScore);
    // console.log(courseName);
 

    // 初始化下拉框的值
    
   
    
    
}
function initCourse(){
    console.log("初始化下拉框");
    document.getElementById("domain").length=0;
    $("#domain").append($("<option></option>").val(0).html("课程类别"));
    for(var idx=0; idx<allSubject.length; idx++){
        $("#domain").append($("<option></option>").val(idx + 1).html(allSubject[idx]));
    }

}
$("#domain").change(function(){
    //初始化课程下拉框
    document.getElementById("course").length=0;
    $("#course").append($("<option></option>").val(0).html("课程"));
    var index = $(this).val()-1;
    // console.log(index);
    // console.log(courseName[0]);
    for(var i = 0; i < courseName[index].length; i++) {
        if(courseScore[index][i] == 0+""){
            $("#course").append($("<option></option>").val(i + 1).html(courseName[index][i]));
        }
          else{
        
            $("#course").append($("<option></option>").val(i + 1).html("√"+courseName[index][i]));
        }
    }
})
$("#course").change(function(){
    //初始化分数值
    document.getElementById("score").length=0;
    document.getElementById("pass").length=0;
    // console.log("pass的长度"+);
    var domainSelect = document.getElementById("domain");
    var domainIndex = domainSelect.selectedIndex-1;
    var courseIndex = $(this).val() - 1;
    // console.log(courseIndex)
    if(courseScore[domainIndex][courseIndex] == 0){
        console.log("未评分");
        $("#score").attr("disabled",false);
        $("#btnScore").attr("disabled",false);
        $("#score").append($("<option></option>").val(0).html("请评分:"));
        for(var s=1; s<=5; s++){
            $("#score").append($("<option></option>").val(s).html(s));
        }
       
     
    }
    else {
        console.log("已评分")
        $("#score").append($("<option></option>").val(0).html("已评分:"+courseScore[domainIndex][courseIndex]));
        $("#score").attr("disabled",true);
    }
    if(coursePass[domainIndex][courseIndex]==0)
    {
        console.log("未判断");
        $("#pass").attr("disabled",false);
        $("#btnScore").attr("disabled",false);
        $("#pass").append($("<option ></option>").val(0).html("是否容易通过"));
        $("#pass").append($("<option value='1'></option>").val(1).html("通过"));
        $("#pass").append($("<option value='0'></option>").val(2).html("不通过"));
        
    }
    else {
        console.log("已判断");
        console.log(coursePass[domainIndex][courseIndex]);
        if(coursePass[domainIndex][courseIndex]==1)
        $("#pass").append($("<option></option>").val(0).html("已判断:通过"));
        else if(coursePass[domainIndex][courseIndex]==2){
            $("#pass").append($("<option></option>").val(0).html("已判断:不通过"));
        }
        $("#pass").attr("disabled",true);
        $("#btnScore").attr("disabled",true);
    }


    
})


// -------------------------------------------------------------------//
// --------------------------------------------------- //
/*
函数(5)：function updataScore()
    更新courseScore
    发送json文件给后端: {"课程1":3."课程2":2, ...}
 */

function updataScore(){
    var domCourse = document.getElementById("course")
    var courseName = domCourse[domCourse.selectedIndex].text;
    var domScore =  document.getElementById("score");
    var pass=document.getElementById('pass');
    var passIndex=pass.selectedIndex-1;
    var tree = myChart.getOption()['series'][0]['data'][0];
    course2score[courseName] = {'score':parseInt(domScore[domScore.selectedIndex].text),"pass":parseInt(pass[pass.selectedIndex].value)};
    console.log(courseName);
    var scores = {};
    scores[courseName] = course2score[courseName];
    var returnData={ "tree":tree,"scores":scores};
   
   $.ajax({
    type:"POST",
    url:"submit_train_plan",
    data:JSON.stringify(returnData),
    success:function(data){
        console.log("data"+(data.score));
        myChart.setOption({
            series:[{
                name:"trianPlanTree",
                data: [data]
            }]
        })
        originTrainPlain = data;
        alert("评分成功");
    },
    error:function(){
        alert("错误");
    }



   })
   
     
    domScore.length=0;
    pass.length=0;
    $("#score").append($("<option></option>").val(0).html("已评分:"+ course2score[courseName].score));
    $("#score").attr("disabled",true);
    if(course2score[courseName].pass==1)
    $('#pass').append($("<option></option>").val(0).html("已判断:通过"));
    else $('#pass').append($("<option></option>").val(0).html("已判断:不通过"));
  
    $("#pass").attr("disabled",true);
   initScore();
   
    // $("#btnScore").attr('disabled',true);
}



setInterval(function(){initScore()}, 3000);
setTimeout(function(){initCourse()},3000); 