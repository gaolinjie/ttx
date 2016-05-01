/**
 * Created by jf on 2015/9/11.
 */

$(function () {

    var pageManager = {
        $container: $('.js_container'),
        _pageStack: [],
        _configs: [],
        _defaultPage: null,
        _pageIndex: 1,
        setDefault: function (defaultPage) {
            this._defaultPage = this._find('name', defaultPage);
            return this;
        },
        init: function () {
            var self = this;

            $(window).on('hashchange', function () {
                var state = history.state || {};
                var url = location.hash.indexOf('#') === 0 ? location.hash : '#';
                var page = self._find('url', url) || self._defaultPage;
                if (state._pageIndex <= self._pageIndex || self._findInStack(url)) {
                    self._back(page);
                } else {
                    self._go(page);
                }
            });

            if (history.state && history.state._pageIndex) {
                this._pageIndex = history.state._pageIndex;
            }

            this._pageIndex--;

            var url = location.hash.indexOf('#') === 0 ? location.hash : '#';
            var page = self._find('url', url) || self._defaultPage;
            this._go(page);
            return this;
        },
        push: function (config) {
            this._configs.push(config);
            return this;
        },
        go: function (to) {
            var config = this._find('name', to);
            if (!config) {
                return;
            }
            location.hash = config.url;
        },
        _go: function (config) {
            this._pageIndex ++;

            history.replaceState && history.replaceState({_pageIndex: this._pageIndex}, '', location.href);

            var html = $(config.template).html();
            var $html = $(html).addClass('slideIn').addClass(config.name);
            this.$container.append($html);
            this._pageStack.push({
                config: config,
                dom: $html
            });

            if (!config.isBind) {
                this._bind(config);
            }

            return this;
        },
        back: function () {
            history.back();
        },
        _back: function (config) {
            this._pageIndex --;

            var stack = this._pageStack.pop();
            if (!stack) {
                return;
            }

            var url = location.hash.indexOf('#') === 0 ? location.hash : '#';
            var found = this._findInStack(url);
            if (!found) {
                var html = $(config.template).html();
                var $html = $(html).css('opacity', 1).addClass(config.name);
                $html.insertBefore(stack.dom);

                if (!config.isBind) {
                    this._bind(config);
                }

                this._pageStack.push({
                    config: config,
                    dom: $html
                });
            }

            stack.dom.addClass('slideOut').on('animationend', function () {
                stack.dom.remove();
            }).on('webkitAnimationEnd', function () {
                stack.dom.remove();
            });

            return this;
        },
        _findInStack: function (url) {
            var found = null;
            for(var i = 0, len = this._pageStack.length; i < len; i++){
                var stack = this._pageStack[i];
                if (stack.config.url === url) {
                    found = stack;
                    break;
                }
            }
            return found;
        },
        _find: function (key, value) {
            var page = null;
            for (var i = 0, len = this._configs.length; i < len; i++) {
                if (this._configs[i][key] === value) {
                    page = this._configs[i];
                    break;
                }
            }
            return page;
        },
        _bind: function (page) {
            var events = page.events || {};
            for (var t in events) {
                for (var type in events[t]) {
                    this.$container.on(type, t, events[t][type]);
                }
            }
            page.isBind = true;
        }
    };

    var home = {
        name: 'home',
        url: '#',
        template: '#tpl_home',
        events: {
            '.js_grid': {
                click: function (e) {
                    var id = $(this).data('id');
                    pageManager.go(id);
                }
            }
        }
    };
    var panel = {
        name: 'panel',
        url: '#panel',
        template: '#tpl_panel'
    };
    var shareit = {
        name: 'shareit',
        url: '#shareit',
        template: '#tpl_shareit',
        events: {
          '#adSelect': {
              click: function (e) {
                var mask = $('#mask');
                var weuiActionsheet = $('#weui_actionsheet');
                weuiActionsheet.addClass('weui_actionsheet_toggle');
                mask.show().addClass('weui_fade_toggle').one('click', function () {
                    hideActionSheet(weuiActionsheet, mask);
                });
                $('#actionsheet_cancel').one('click', function () {
                    hideActionSheet(weuiActionsheet, mask);
                });
                $('.weui_actionsheet_menu .weui_actionsheet_cell').one('click', function () {
                    var cellText = $(this).text();
                    var cellUuid = $(this).attr('data-uuid');
                    $('#adSelect .weui_cell_bd p').text(cellText);
                    $('#adSelect').attr('data-uuid', cellUuid);
                    hideActionSheet(weuiActionsheet, mask);
                });
                weuiActionsheet.unbind('transitionend').unbind('webkitTransitionEnd');

                function hideActionSheet(weuiActionsheet, mask) {
                    weuiActionsheet.removeClass('weui_actionsheet_toggle');
                    mask.removeClass('weui_fade_toggle');
                    weuiActionsheet.on('transitionend', function () {
                        mask.hide();
                    }).on('webkitTransitionEnd', function () {
                        mask.hide();
                    })
                }
              }
          },
          '#shareIt': {
              click: function (e) {
                  var $linkText = $('#linkText').val();
                  var $adUuid = $('#adSelect').attr('data-uuid');
                  $.ajax({
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    url: "/shareit",
                    data: JSON.stringify({
                      link_text: $linkText,
                      ad_uuid: $adUuid,
                    }),
                    success: function(msg) {
                      if (msg.success != 0) {
                        //alert(msg.topic_url);
                        window.location.replace(msg.topic_url);
                      } else {
                        alert("error");
                      }
                    },
                    error: function(msg) {
                      alert("error");
                    }
                  });
              }
          }
        }
    };
    var addad = {
        name: 'addad',
        url: '#addad',
        template: '#tpl_addad',
        events: {
          '#adTemplate': {
              click: function (e) {
                var mask = $('#mask');
                var weuiActionsheet = $('#weui_actionsheet');
                weuiActionsheet.addClass('weui_actionsheet_toggle');
                mask.show().addClass('weui_fade_toggle').one('click', function () {
                    hideActionSheet(weuiActionsheet, mask);
                });
                $('#actionsheet_cancel').one('click', function () {
                    hideActionSheet(weuiActionsheet, mask);
                });
                $('.weui_actionsheet_menu .weui_actionsheet_cell').one('click', function () {
                    var cellText = $(this).text();
                    $('#adTemplate .weui_cell_bd p').text(cellText);
                    hideActionSheet(weuiActionsheet, mask);
                });
                weuiActionsheet.unbind('transitionend').unbind('webkitTransitionEnd');

                function hideActionSheet(weuiActionsheet, mask) {
                    weuiActionsheet.removeClass('weui_actionsheet_toggle');
                    mask.removeClass('weui_fade_toggle');
                    weuiActionsheet.on('transitionend', function () {
                        mask.hide();
                    }).on('webkitTransitionEnd', function () {
                        mask.hide();
                    })
                }
              }
          },
          '#addAd': {
              click: function (e) {
                  var $ad_name = $('#adName').val();
                  var $ad_type = $('#adTemplate .weui_cell_primary p').text();
                  var $ad_text = $('#adText').val();
                  var $ad_link = $('#adLink').val();
                  $.ajax({
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    url: "/addad",
                    data: JSON.stringify({
                      ad_name: $ad_name,
                      ad_type: $ad_type,
                      ad_text: $ad_text,
                      ad_link: $ad_link,
                    }),
                    success: function(msg) {
                      if (msg.success != 0) {
                        //alert(msg.topic_url);
                        window.location.replace('/');
                      } else {
                        alert("error");
                      }
                    },
                    error: function(msg) {
                      alert("error");
                    }
                  });
              }
          }
        }
    };
    var addtb = {
        name: 'addtb',
        url: '#addtb',
        template: '#tpl_addtb',
        events: {
          '#addTb': {
              click: function (e) {
                  var $linkText = $('#linkText').val();
                  var re = new RegExp('https:\/\/(.+).taobao.com');
                  var shop_type = '';
                  var shop_link = '';
                  if (re.exec($linkText)) {
                    shop_link = re.exec($linkText)[0];
                    shop_type = 'taobao';
                  } else {
                    re = new RegExp('https:\/\/(.+).tmall.com');
                    if (re.exec($linkText)) {
                        shop_link = re.exec($linkText)[0];
                        shop_type = 'tmall';
                    }
                  }

                  if ('' == shop_link) {
                    return;
                  }
                  
                  shop_link = shop_link.replace('https://', '');
                  var default_url = 'https://'+ shop_link + "/i/asynSearch.htm?mid=w-9918988062-0&wid=9918988062&path=/category.htm&search=y&orderType=hotsell_desc&pageNo=";
                  var shop_uuid = "";
                  var page = 1;
                  var url = default_url + page;
                  getShopUUID(shop_link, shop_type);
                  getItems(url);

                  function getShopUUID(shop_link, shop_type) {
                    $.getJSON('/get/shop?shop_link=' + shop_link + '&shop_type=' + shop_type, function(data) {
                      if (data.success != 0) {
                        shop_uuid = data.shop_uuid;
                      } else {
                        alert('获取店铺UUID失败，请重试!');
                      }
                    });
                  }

                  function getItems(url) {
                    $.ajax({
                      url: url,
                      type: "GET",
                      dataType: 'jsonp',
                      crossDomain: true,
                      success: function(msg){
                        if (msg.search('没找到符合条件的商品') == -1) {
                          postItems(msg);
                        }
                      },
                      error: function(msg) {
                        alert("error");
                      }
                    });
                  }

                  function postItems(items) {
                    $.ajax({
                      type: "POST",
                      contentType: "application/json; charset=utf-8",
                      dataType: "json",
                      url: "/addtb",
                      data: JSON.stringify({
                        item_type: shop_type,
                        shop_uuid: shop_uuid,
                        items_text: items,
                      }),
                      success: function(msg) {
                        page = page + 1;
                        getItems(default_url + page);
                      },
                      error: function(msg) {
                        alert("error");
                      }
                    });
                  }
              }
          }
        }
    };
    var button = {
        name: 'button',
        url: '#button',
        template: '#tpl_button'
    };
    var cell = {
        name: 'cell',
        url: '#cell',
        template: '#tpl_cell',
        events: {
            '#showTooltips': {
                click: function () {
                    var $tooltips = $('.js_tooltips');
                    if ($tooltips.css('display') != 'none') {
                        return;
                    }

                    // 如果有`animation`, `position: fixed`不生效
                    $('.page.cell').removeClass('slideIn');
                    $tooltips.show();
                    setTimeout(function () {
                        $tooltips.hide();
                    }, 2000);
                }
            }
        }
    };
    var toast = {
        name: 'toast',
        url: '#toast',
        template: '#tpl_toast',
        events: {
            '#showToast': {
                click: function (e) {
                    var $toast = $('#toast');
                    if ($toast.css('display') != 'none') {
                        return;
                    }

                    $toast.show();
                    setTimeout(function () {
                        $toast.hide();
                    }, 2000);
                }
            },
            '#showLoadingToast': {
                click: function (e) {
                    var $loadingToast = $('#loadingToast');
                    if ($loadingToast.css('display') != 'none') {
                        return;
                    }

                    $loadingToast.show();
                    setTimeout(function () {
                        $loadingToast.hide();
                    }, 2000);
                }
            }
        }
    };
    var dialog = {
        name: 'dialog',
        url: '#dialog',
        template: '#tpl_dialog',
        events: {
            '#showDialog1': {
                click: function (e) {
                    var $dialog = $('#dialog1');
                    $dialog.show();
                    $dialog.find('.weui_btn_dialog').one('click', function () {
                        $dialog.hide();
                    });
                }
            },
            '#showDialog2': {
                click: function (e) {
                    var $dialog = $('#dialog2');
                    $dialog.show();
                    $dialog.find('.weui_btn_dialog').one('click', function () {
                        $dialog.hide();
                    });
                }
            }
        }
    };
    var progress = {
        name: 'progress',
        url: '#progress',
        template: '#tpl_progress',
        events: {
            '#btnStartProgress': {
                click: function () {

                    if ($(this).hasClass('weui_btn_disabled')) {
                        return;
                    }

                    $(this).addClass('weui_btn_disabled');

                    var progress = 0;
                    var $progress = $('.js_progress');

                    function next() {
                        $progress.css({width: progress + '%'});
                        progress = ++progress % 100;
                        setTimeout(next, 30);
                    }

                    next();
                }
            }
        }
    };
    var msg = {
        name: 'msg',
        url: '#msg',
        template: '#tpl_msg',
        events: {}
    };
    var article = {
        name: 'article',
        url: '#article',
        template: '#tpl_article',
        events: {}
    };
    var tab = {
        name: 'tab',
        url: '#tab',
        template: '#tpl_tab',
        events: {
            '.js_tab': {
                click: function (){
                    var id = $(this).data('id');
                    pageManager.go(id);
                }
            }
        }
    };
    var navbar = {
        name: 'navbar',
        url: '#navbar',
        template: '#tpl_navbar',
        events: {}
    };
    var tabbar = {
        name: 'tabbar',
        url: '#tabbar',
        template: '#tpl_tabbar',
        events: {}
    };
    var actionSheet = {
        name: 'actionsheet',
        url: '#actionsheet',
        template: '#tpl_actionsheet',
        events: {
            '#showActionSheet': {
                click: function () {
                    var mask = $('#mask');
                    var weuiActionsheet = $('#weui_actionsheet');
                    weuiActionsheet.addClass('weui_actionsheet_toggle');
                    mask.show().addClass('weui_fade_toggle').one('click', function () {
                        hideActionSheet(weuiActionsheet, mask);
                    });
                    $('#actionsheet_cancel').one('click', function () {
                        hideActionSheet(weuiActionsheet, mask);
                    });
                    weuiActionsheet.unbind('transitionend').unbind('webkitTransitionEnd');

                    function hideActionSheet(weuiActionsheet, mask) {
                        weuiActionsheet.removeClass('weui_actionsheet_toggle');
                        mask.removeClass('weui_fade_toggle');
                        weuiActionsheet.on('transitionend', function () {
                            mask.hide();
                        }).on('webkitTransitionEnd', function () {
                            mask.hide();
                        })
                    }
                }
            }
        }
    };
    var searchbar = {
        name:"searchbar",
        url:"#searchbar",
        template: '#tpl_searchbar',
        events:{
            '#search_input':{
                focus:function(){
                    //searchBar
                    var $weuiSearchBar = $('#search_bar');
                    $weuiSearchBar.addClass('weui_search_focusing');
                },
                blur:function(){
                    var $weuiSearchBar = $('#search_bar');
                    $weuiSearchBar.removeClass('weui_search_focusing');
                    if($(this).val()){
                        $('#search_text').hide();
                    }else{
                        $('#search_text').show();
                    }
                },
                input:function(){
                    var $searchShow = $("#search_show");
                    if($(this).val()){
                        $searchShow.show();
                    }else{
                        $searchShow.hide();
                    }
                }
            },
            "#search_cancel":{
                touchend:function(){
                    $("#search_show").hide();
                    $('#search_input').val('');
                }
            },
            "#search_clear":{
                touchend:function(){
                    $("#search_show").hide();
                    $('#search_input').val('');
                }
            }
        }
    };
    var icons = {
        name: 'icons',
        url: '#icons',
        template: '#tpl_icons',
        events: {}
    };

    pageManager.push(home)
        .push(shareit)
        .push(addad)
        .push(addtb)
        .push(cell)
        .push(toast)
        .push(dialog)
        .push(progress)
        .push(msg)
        .push(article)
        .push(tab)
        .push(navbar)
        .push(tabbar)
        .push(panel)
        .push(actionSheet)
        .push(icons)
        .push(searchbar)
        .setDefault('home')
        .init();
});
