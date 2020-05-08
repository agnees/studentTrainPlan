
function getpassword(){
  console.log("1");
  var email=document.getElementById('email').value;

  var startyear=document.getElementById('year').value;
  var returnData={
    "stu_no":email,
    "ad_year":startyear
  }
  $.ajax({
   type:'post',
   url:'get_user_info',
   data:JSON.stringify(returnData),
   success:function(data){
       alert("账号："+data.stu_no+"  密码："+data.password);
      
   }
   ,error:function(){
    alert("输入错误");
   }
   
   




  })

}
