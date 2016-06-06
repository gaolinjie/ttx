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
        
        var shopUrl=$("body").attr("data-src");
        
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
    $(document).on('click', '.beatHeader', function() {
      toggleBeatHeader();
    });
    $(document).on('click', 'body', function() {
      toggleBeatHeader();
    });
       
    });