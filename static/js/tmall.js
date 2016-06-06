$(function(){
        function is_weixin() {
            var ua = navigator.userAgent.toLowerCase();
            if (ua.match(/MicroMessenger/i) == "micromessenger") {
                return true;
            } else {
                return false;
            }
        }
        var isWeixin = is_weixin();
        var os_type="iPhone";
        
        var sku = $("body").attr("data-sku");
        var shopUrl="https://detail.m.tmall.com/item.htm?id="+sku;
        
        if(isWeixin){

        } else {
            if (os_type=="android") {
                openIphoneApp(shopUrl); 
            } else if (os_type=="iPhone_ios_9") {
                openIphoneApp_ios_9(shopUrl); 
            } else {
                openIphoneApp(shopUrl); 
            }
        }

        function openIphoneApp(url){
            // 通过iframe的方式试图打开APP，如果能正常打开，会直接切换到APP，并自动阻止a标签的默认行为  
            // 否则打开a标签的href链接  
            var tb_url=url.replace("http://", "").replace("https://", "");
            var ifr = document.createElement('iframe');  
            ifr.src = 'taobao://'+tb_url;  
            ifr.style.display = 'none';  
            document.body.appendChild(ifr);  
            window.location=url;
        }

        function openIphoneApp_ios_9(url){
            var tb_url=url.replace("http://", "").replace("https://", "");
            window.location="taobao://"+tb_url;
            window.setTimeout(function(){  
                window.location=url; 
            },4000);
        }

        $(".dtct-ul li:eq(0)").click(function(){
            $(this).attr("class", "sel");
            $(".dtct-ul li:eq(1)").attr("class", "");
            $(".dtct-ul li:eq(2)").attr("class", "");
            $(".dt-param").hide();
            $(".dt-comt").hide();
            $(".dt-imgtext").show();
            
        })
        $(".dtct-ul li:eq(1)").click(function(){
            $(this).attr("class", "sel");
            $(".dtct-ul li:eq(0)").attr("class", "");
            $(".dtct-ul li:eq(2)").attr("class", "");
            $(".dt-imgtext").hide();
            $(".dt-comt").hide();
            $(".dt-param").show();
        })
            
        $(".dtct-ul li:eq(2)").click(function(){
            $(this).attr("class", "sel");
            $(".dtct-ul li:eq(0)").attr("class", "");
            $(".dtct-ul li:eq(1)").attr("class", "");
            $(".dt-imgtext").hide();
            $(".dt-param").hide();
            $(".dt-comt").show();
        })

        $("img").lazyload();



        function toggleBeatHeader() {
        var ua = navigator.userAgent.toLowerCase();
        if (/iphone|ipad|ipod/.test(ua)) {
            //alert("ios");
            $(".beatHeader").css({"background": "url(http://mmm-static.qiniudn.com/prompt-ios.jpg) no-repeat #494A4D", "background-size": "contain", "background-position": "50% 50%"});
        } else if (/android/.test(ua)) {
            //alert("android");
            $(".beatHeader").css({"background": "url(http://mmm-static.qiniudn.com/prompt-android.jpg) no-repeat #494A4D", "background-size": "contain", "background-position": "50% 50%"});
        } 
      $(".beatHeader").toggle();
    }
    
    $(document).on('click', '#detail-base-smart-banner', function() {
      //var link = $(this).attr("data-link");
      //window.location.href="/prompt?url=" + link;
      toggleBeatHeader();
    });

    $(document).on('click', '#s-actionBar-container', function() {
        //var link = $(this).attr("data-link");
      //window.location.href="/prompt?url=" + link;
      toggleBeatHeader();
    });
    $(document).on('click', '.beatHeader', function() {
      toggleBeatHeader();
    });
       
    });