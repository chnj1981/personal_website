var log = function () {
    console.log(arguments)
}

var timestampProcess = function (unix_time) {
    var d = new Date(unix_time * 1000)
    var vYear = d.getFullYear()
    var vMon = d.getMonth() + 1
    var vDay = d.getDate()
    var h = d.getHours()
    var m = d.getMinutes()
    var se = d.getSeconds()
    now = vYear + "-" + (vMon < 10 ? "0" + vMon : vMon) + "-" + (vDay < 10 ? "0" + vDay : vDay) + " " + (h < 10 ? "0" + h : h) + ":" + (m < 10 ? "0" + m : m) + ":" + (se < 10 ? "0" + se : se)
    return now
}

var formatTimestamp = function () {
    $(".timestamp").each(function () {
        var self = $(this)
        var t = timestampProcess(parseInt(self.html()))
        self.html(t)
    });
}

var goTop = function () {
    var top = $("#gotop")
    top.click(function (e) {
        $('body,html').animate({scrollTop: 0}, 1000);
    });

    top.mouseover(function (e) {
        $(this).css("background", "url(http://oexqautw4.bkt.clouddn.com/static/img/backtop.png) no-repeat 0px 0px");
        $(this).css('cursor', 'pointer');
        $(this).css('opacity', '1');
    });

    top.mouseout(function (e) {
        $(this).css("background", "url(http://oexqautw4.bkt.clouddn.com/static/img/backtop.png) no-repeat -70px 0px");
        $(this).css("opacity", "0.5");
    });

    $(window).scroll(function (e) {
        if ($(window).scrollTop() > 1000)
            $("#gotop").fadeIn(1000);
        else
            $("#gotop").fadeOut(1000);
    });
}

var checkSubmit = function (input, btn, min_l = 1) {
    var all = $(input)
    all.each(function () {
        $(this).keyup(function () {
            text = $(this).val()
            var len = $.trim(text).length
            var b = $(this).siblings(btn)
            if (len < min_l) {
                b.addClass("disabled");
            } else {
                b.removeClass("disabled");
            }

        })
    })
}

var htmlToMarkdown = function (html) {
    var converter = new showdown.Converter();
    converter.setOption("tasklists", true);
    converter.setOption("tables", true);
    var self = $(html)
    self.html(converter.makeHtml(self.text()))
}

var longTimeAgo = function () {
    var timeAgo = function (time, ago) {
        return Math.round(time) + ago;
    };
    $('.timestamp').each(function (i, e) {
        var past = parseInt($(e).text());
        var now = Math.round(new Date().getTime() / 1000);
        var seconds = now - past;
        var ago = seconds / 60;
        var oneHour = 60;
        var oneDay = oneHour * 24;
        var oneMonth = oneDay * 30;
        var oneYear = oneMonth * 12;
        var s = '';
        if (seconds < 60) {
            s = timeAgo(seconds, ' 秒前')
        } else if (ago < oneHour) {
            s = timeAgo(ago, ' 分钟前');
        } else if (ago < oneDay) {
            s = timeAgo(ago / oneHour, ' 小时前');
        } else if (ago < oneMonth) {
            s = timeAgo(ago / oneDay, ' 天前');
        } else if (ago < oneYear) {
            s = timeAgo(ago / oneMonth, ' 月前');
        }
        $(e).text(s);
    });
};

var codeHighlight = function () {
    hljs.initHighlightingOnLoad()
}
