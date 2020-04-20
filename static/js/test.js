$(document).ready(function() {

 

    $('.setPageDiv').change(function() {
    
    
    
        getMsg(parseInt($(this).val()))
    
    });
 
    
    
    function getMsg(num) 
    {
    //   console.log(num);
  

      $.ajax({
            url:'news_center',
            type:'POST',
            dataType:'json',
   
             success: function(data) {
    
                
                
                //1.计算分页数量
                
       
                var showNum = num;
                
                
                
                var dataL=data.length;
               
                var pageNum = Math.ceil(data.length / showNum);
                console.log("页数"+pageNum);
    
                $('.pagination').pagination(pageNum, {

    
                    num_edge_entries: 1, //边缘页数
    
                    num_display_entries: 4, //主体页数
    
                    items_per_page: 1, //每页显示1项
    
                    prev_text: "上一页",
    
                    next_text: "下一页",
    
                    callback: function(index) {
    
                        console.log("callback");
    
                        var html = '<ul class="content_boxL_list">'
    
    
    
                        console.log(showNum * index + '~' + parseInt(showNum * index) + parseInt(showNum))
    
                        for(var i = showNum * index; i < showNum * index + showNum; i++) {
    
                            //console.log(i)
    
                            if(i < dataL) {
                             var adata=data[i][4];
                             var name=data[i][2];
                             var time=data[i][3];
                             var title=data[i][0];
                             var content=data[i][1];
                             html+='<li> <a class="content_boxL_list_info" href="detail/'+adata+'">'+
                             name+":["+title+"]"+content+'<span class="yewu_date">'+time+'</span></a></li>';
    
                                
                                
    
    
                            }
    
                        }
    
                        html += '</ul>';
    
                        $('.list').html(html)
    
                    }
    
                })
    
    
    
            }
            
            ,
            error:function(data){
            //  alert(XMLResponse.states);
            //   alert("错误"+this.getStatus());
            alert("服务器返回错误,请重试");
            }
        });
    
    }
    
    getMsg(6);
})
    
    
    
    
    
    
    
    
    
  
    
    