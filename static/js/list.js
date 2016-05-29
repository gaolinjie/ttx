$(function(){
        //$("img").lazyload();
        
    var pageNum = 1;

    // dropload
    $('.rich_media_area_primary').dropload({
        scrollArea : window,
        loadDownFn : function(me){
            $.ajax({
                type: 'GET',
                url: '/baicai/items?p='+pageNum,
                dataType: 'json',
                success: function(data){

                    var result = '';
                    for(var i = 0; i < data.list.length; i++){
                        result += '<li><a href="/p/'+data.list[i].id+'" target="_blank" class="hidden openApp"><div class="image_wrap"><div class="image"><img src="http://www.zorhand.com/img?url='+data.list[i].thumb+'" alt="'+data.list[i].title+'"></div></div><address><span>'+data.list[i].created+'</span>'+data.list[i].vendor+'</address><h2>'+data.list[i].title+'</h2><div class="tips"><em>'+data.list[i].subtitle+'</em></div></a></li>';
                    }

                        $('.list').append(result);
                        // 每次数据加载完，必须重置
                        me.resetload();

                        pageNum++;
                        if (pageNum > data.page.pages) {
                            me.lock();
                            me.noData();
                        }

                },
                error: function(xhr, type){
                    alert('Ajax error!');
                    // 即使加载出错，也得重置
                    me.resetload();
                }
            });
        }
    });
});