$(document).ready(function() {

    $("a").each(function() {
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

            if (seller_id != null) {
              $(this).css({"color":"#f04848", 
                "background-color":"#f5f5f5",
                "border-radius":"2px",
                "text-align":"center", 
                "padding": "0 2px",
                "margin-right": "2px"});

              //$(this).attr('href', 'http://djaa.cn/iphone_qiange_discount.php?shopUrl=https%3A%2F%2Ftmall.m.taobao.com%2Fshop%2Fcoupon.htm%3Fseller_id%3D'+seller_id+'%26activity_id%3D'+activity_id+'&shop_type=taobao&Advertisement=0&small_shop_type=discount');
            $(this).attr('href', '/coupon?url=https%3A%2F%2Ftmall.m.taobao.com%2Fshop%2Fcoupon.htm%3Fseller_id%3D'+seller_id+'%26activity_id%3D'+activity_id+'&shop_type=taobao&Advertisement=0&small_shop_type=discount');
            }
        
    });
});