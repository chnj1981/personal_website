var log = function () {
    console.log(arguments)
}

var weiboTemplate = function (w) {
    return `
<div class="wb-item col-xs-12 border-std shadow" data-id="${ w.id }">
    <div class="wb-main row">
        <div class="col-xs-1">
            <img class="img-m img-rounded" src="${ w.avatar }">
        </div>
        <div class="col-xs-10 wb-info">
            <div class=""><a href="${ "/user/profile/" +  w.user_id }" >${ w.nickname }</a></div>
            <span>发布于: </span><span class="timestamp" >${ timestampProcess(w.created_time) }</span>
            <p class="wb-content">${ w.weibo }</p>
        </div>
    </div>

    <div class="wb-nav row">
        <ul class="nav nav-tabs" role="tablist">
            <li><a href="#" class="btn-comment-show">评论 (<span
                class="comments_num">${ w.comments_num }</span>)</a></li>
            <li><a href="#" class="btn-wb-like">赞 (<span>0</span>)</a></li>
            <li><a href="#" class="btn-wb-update-show">修改</a></li>
        </ul>
    </div>


    <div class="wb-update" style="display: none;">
        <textarea class="form-control  input-wb-update  " maxlength="200"rows="3">${ w.weibo }</textarea>
        <h4><span class="label label-danger">微博更新时间间隔至少一小时, 写这句话的人除外 </span></h4>
        <a href="#" class="btn-wb-update-submit btn btn-warning btn-block disabled">提交</a>
    </div>

    <div class="wb-comment" style="display: none;">

        <div class="wb-comment-add">
            <textarea class="form-control input-wb-comment "  maxlength="100" rows="2" placeholder="100字以内"></textarea>
            <a class="btn btn-primary btn-wb-comment-add btn-block disabled">批判一番</a>
        </div>

        <div class="wb-comment-cells">

        </div>

    </div><script>checkInput()</script>

</div>
`
}

var bindEventCommentToggle = function () {
    $('.wb-cells').on('click', '.btn-comment-show', function () {
        var grandpa = $(this).closest('.wb-item');
        grandpa.find('.wb-update').css('display', 'none');
        grandpa.find('.wb-comment').slideToggle('slow');

        var ul = grandpa.find('.nav-tabs')
        var p = $(this).parent();
        p.siblings().removeClass("active");
        if (p.hasClass("active")) {
            p.removeClass("active");
            ul.removeClass('fuck-nav')
        } else {
            p.addClass("active")
            ul.addClass('fuck-nav')
        }
        return false
    })
}

var bindEventUpdateToggle = function () {
    $('.wb-cells').on('click', '.btn-wb-update-show', function () {
        var grandpa = $(this).closest('.wb-item');
        grandpa.find('.wb-comment').css('display', 'none');
        grandpa.find('.wb-update').slideToggle('slow');

        var ul = grandpa.find('.nav-tabs')
        var p = $(this).parent();
        p.siblings().removeClass("active");
        if (p.hasClass("active")) {
            p.removeClass("active");
            ul.removeClass('fuck-nav')
        } else {
            p.addClass("active")
            ul.addClass('fuck-nav')
        }
        return false;
    })
};

var bindEventWeiboUpdate = function () {
    $('.wb-cells').on('click', '.btn-wb-update-submit', function () {
        if ($(this).hasClass('disabled')) return false
        var w = $(this).closest('.wb-item');
        var update = w.find('.input-wb-update');
        var old = w.find('.wb-content');
        var btn = $('.btn-wb-update-show').parent()
        var weibo_id = w.data('id');
        var self = $(this)

        content = filterXSS(update.val());
        var form = {
            weibo_id: weibo_id,
            content: content
        }
        var response = function (r) {
            if (r.success) {
                old.html(content)
                old.hide().slideToggle('slow')
                w.find('.wb-update').slideToggle('slow')
                btn.removeClass('active')
                self.addClass('disabled')

            } else {
                alert(r.message)
            }
        }
        api.weiboUpdate(form, response)
        return false
    })
}

var checkUpdate = function () {
    var update = $('.input-wb-update');
    var old = $('.wb-content');
    for (i = 0; i < update.length; i++) {
        if (update[i].val() == old.text()) {
            update[i].next().addClass('disabled')
        }
    }
}

var bindEventWeiboAdd = function () {
    $('.btn-wb-add').on('click', function () {
        if ($(this).hasClass('disabled')) return false
        var input = $('.input-wb-new')
        var w = input.val()
        var btn = $(this)
        var weibo = filterXSS(w)
        var form = {
            weibo: weibo
        }

        var response = function (r) {
            if (r.success) {
                var new_weibo = $(weiboTemplate(r.data))
                var weibo_container = $('.wb-cells')[1]
                new_weibo.hide().prependTo(weibo_container).slideDown('slow');
                input.val('')
                btn.addClass('disabled')
            } else {
                alert(r.message)
            }
        }
        api.weiboAdd(form, response)
        return false
    })
}

var bindEventWeiboDelete = function () {
    $('.wb-cells').on('click', '.btn-wb-delete', function () {
        var weibo = $(this).closest('.wb-item')
        var weiboId = weibo.data('id')
        var response = function (r) {
            if (r.success) {
                $(weibo).slideToggle('slow')
            } else {
                alert(r.message)
            }
        }
        api.weiboDelete(weiboId, response)
        return false
    })
}


var commentTemplate = function (c) {
    return `
<div class="row wb-comment-item">
    <div class="col-xs-1">
        <img class="img-s img-rounded" src="${ c.avatar }">
    </div>
    <div class="col-xs-10">
        <p>
            <a href="${ "/user/profile/" +  c.user_id }">${ c.nickname }</a><span> : </span>${ c.comment }
        </p>
        <span class="timestamp">${ timestampProcess(c.created_time) }</span>
    </div>
</div>
`
}

var bindEventWeiboCommentAdd = function () {
    $('.wb-cells').on('click', ".btn-wb-comment-add", function () {
        if ($(this).hasClass('disabled')){
            return false
        }

        var comment = $(this).parent().find('.input-wb-comment')
        var weibo = $(this).closest('.wb-item')
        var form = {
            comment: filterXSS(comment.val()),
            weibo_id: weibo.data('id')
        };

        var self = $(this)
        var comment_div = $(this).closest('.wb-comment').find('.wb-comment-cells');
        var response = function (r) {
            if (r.success) {
                new_comment = commentTemplate(r.data);
                $(new_comment).hide().prependTo(comment_div).slideDown('slow');
                var num = weibo.find('.comments_num');
                var a = parseInt(num.text());
                num.text(a + 1);
                comment.val('')
                self.addClass('disabled')
            } else {
                alert(r.message)
            }
        }
        api.weiboCommentAdd(form, response)
    })
}

var color_blind = function () {
    var c = ["#DC143C", "#FFF0F5", "#DB7093", "#FF69B4", "#FF1493", "#C71585", "#DA70D6", "#D8BFD8", "#DDA0DD", "#EE82EE", "#FF00FF", "#FF00FF", "#8B008B", "#800080", "#BA55D3", "#9400D3", "#9932CC", "#4B0082", "#8A2BE2", "#9370DB", "#7B68EE", "#6A5ACD", "#483D8B", "#E6E6FA", "#F8F8FF", "#0000FF", "#0000CD", "#191970", "#00008B", "#000080", "#4169E1", "#6495ED", "#B0C4DE", "#778899", "#708090", "#1E90FF", "#F0F8FF", "#4682B4", "#87CEFA", "#87CEEB", "#00BFFF", "#ADD8E6", "#B0E0E6", "#5F9EA0", "#F0FFFF", "#E0FFFF", "#AFEEEE", "#00FFFF", "#00FFFF", "#00CED1", "#2F4F4F", "#008B8B", "#008080", "#48D1CC", "#20B2AA", "#40E0D0", "#7FFFD4", "#66CDAA", "#00FA9A", "#F5FFFA", "#00FF7F", "#3CB371", "#2E8B57", "#F0FFF0", "#90EE90", "#98FB98", "#8FBC8F", "#32CD32", "#00FF00", "#228B22", "#008000", "#006400", "#7FFF00", "#7CFC00", "#ADFF2F", "#556B2F", "#9ACD32", "#6B8E23", "#F5F5DC", "#FAFAD2", "#FFFFF0", "#FFFFE0", "#FFFF00", "#808000", "#BDB76B", "#FFFACD", "#EEE8AA", "#F0E68C", "#FFD700", "#FFF8DC", "#DAA520", "#B8860B", "#FFFAF0", "#FDF5E6", "#F5DEB3", "#FFE4B5", "#FFA500", "#FFEFD5", "#FFEBCD", "#FFDEAD", "#FAEBD7", "#D2B48C", "#DEB887", "#FFE4C4", "#FF8C00", "#FAF0E6", "#CD853F", "#FFDAB9", "#F4A460", "#D2691E", "#8B4513", "#FFF5EE", "#A0522D", "#FFA07A", "#FF7F50", "#FF4500", "#E9967A", "#FF6347", "#FFE4E1", "#FA8072", "#FFFAFA", "#F08080", "#BC8F8F", "#CD5C5C", "#FF0000", "#A52A2A", "#B22222", "#8B0000", "#800000", "#FFFFFF", "#F5F5F5", "#DCDCDC", "#D3D3D3", "#C0C0C0", "#A9A9A9", "#808080", "#696969", "#000000"]
    var back = $('.billboard');
    var i = Math.round(Math.random() * c.length)
    back.css('background', c[i])
}
var blindId = 0

var blindEye = function () {
    blindId = setInterval("color_blind()", 100)
}

var bindEventCallDJ = function () {
    $('.btn-fuck-dj').on('click', function () {
        var music = document.getElementById('fuck-music')
        var foo = $('div.fuck-dj')
        if (music.paused) {
            music.play()
            $(this).text("依依不舍的送走DJ")
            blindEye()
        } else {
            music.pause()
            $(this).text('我爱DJ, 戴上墨镜再次呼叫DJ !')
            clearInterval(blindId)
            $('.billboard').css('background', 'white')
        }
        foo.slideToggle('slow')
    })
}

var checkInput = function () {
    checkSubmit('.input-wb-new', '.btn-wb-add', 3)
    checkSubmit('.input-wb-update', '.btn-wb-update-submit', 3)
    checkSubmit('.input-wb-comment', '.btn-wb-comment-add', 1)
}

var weiboLike = function () {
    $('.wb-cells').on('click', '.btn-wb-like', function () {
        var weibo = $(this).closest('.wb-item')
        var weiboId = weibo.data('id')
        var self = $(this)
        var nums = self.children()
        var response = function (r) {
            if (r.success) {
                nums.text(r.data.like_nums)
            } else {
                alert('未知异常, 点赞失败')
            }
        }
        api.weiboLike(weiboId, response)
        return false
    })
}

var bindEvents = function () {
    formatTimestamp()
    goTop()
    checkInput()
    weiboLike()
    bindEventUpdateToggle()
    bindEventCommentToggle()
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboCommentAdd()
    bindEventWeiboUpdate()
    bindEventCallDJ()
}

$(document).ready(function () {
    bindEvents()
})
