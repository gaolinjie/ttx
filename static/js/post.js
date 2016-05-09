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
        if (text.indexOf("优惠券")!=-1 || text.indexOf("优惠劵")!=-1 || text.indexOf("店铺券")!=-1) {
            $(this).css({"color":"#f04848", "background-color":"#f5f5f5","border-radius":"2px","text-align":"center", "padding": "0 2px"});
        }
    });
});
