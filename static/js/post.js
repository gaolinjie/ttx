$(document).ready(function() {
  $(".video_iframe").each(function() {
        var width = document.body.clientWidth - 30;
        var height = width/1.33;
        $(this).width(width);
        $(this).height(height);
        $(this).attr('width', width);
        $(this).attr('height', height);
        var video_src = $(this).attr('data-src');
        var p1 = video_src.indexOf('vid=');
        var video_vid = video_src.substring(p1+4, video_src.indexOf('&'), p1);
        video_src = "http://v.qq.com/iframe/player.html?vid=" + video_vid + "&amp;width=" + width + "&amp;height=" + height + "&amp;auto=0";
        $(this).attr('src', video_src);
    });

    $("img").lazyload();

    $("a").each(function() {
        var text = $(this).text();
        if (text.indexOf("优惠券")!=-1 || text.indexOf("优惠劵")!=-1 || 
            text.indexOf("店铺券")!=-1 || text.indexOf("元券")!=-1 || 
            text.indexOf("现金卷")!=-1 || text.indexOf("现金券")!=-1 ||
            text.indexOf("元劵")!=-1 || text.indexOf("元优惠")!=-1 ||
            text.indexOf("优惠卷") != -1) {
            $(this).css({"color":"#f04848", 
                "background-color":"#f5f5f5",
                "border-radius":"2px",
                "text-align":"center", 
                "padding": "0 2px",
                "margin-right": "2px"});

            var link = $(this).attr('href');
            var seller_id;
            var activity_id;
            var result = link.match(/seller_id=(\d*)/); 
            if (result != null) { 
                seller_id = result[1]; 
            }
            result = link.match(/activity_id=(\w*)/); 
            if (result != null) { 
                activity_id = result[1]; 
            }
            if (seller_id == null) {
                result = link.match(/sellerId%3D(\d*)/); 
                if (result != null) { 
                    seller_id = result[1]; 
                }
                result = link.match(/activityId%3D(\w*)/); 
                if (result != null) { 
                    activity_id = result[1]; 
                }
            }
            if (seller_id == null) {
                result = link.match(/sellerId=(\d*)/); 
                if (result != null) { 
                    seller_id = result[1]; 
                }
                result = link.match(/activityId=(\w*)/); 
                if (result != null) { 
                    activity_id = result[1]; 
                }
            }
            if (seller_id == null) {
                result = link.match(/sellerId%3D(\d*)/); 
                if (result != null) { 
                    seller_id = result[1]; 
                }
                result = link.match(/activityId%3D(\w*)/); 
                if (result != null) { 
                    activity_id = result[1]; 
                }
            }

            $(this).attr('href', 'http://djaa.cn/iphone_qiange_discount.php?shopUrl=https%3A%2F%2Ftmall.m.taobao.com%2Fshop%2Fcoupon.htm%3Fseller_id%3D'+seller_id+'%26activity_id%3D'+activity_id+'&shop_type=taobao&Advertisement=0&small_shop_type=discount');
        }
    });
});
