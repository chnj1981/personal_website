var commentTemplate = function (c) {
    return `
<div class="comment-item row">
    <div class="col-xs-1 u-avatar"><img src=${ c.avatar } class="img-l img-rounded"></div>
    <div class="col-xs-8 u-comment">
        <p>${ c.nickname }</p>
        <p class="comment-content">${ c.content }</p>
        <p class="timestamp">${ timestampProcess(c.created_time) }</p>
    </div>
    <script>
        var self = $('.comment-content').first()

        var converter = new showdown.Converter();
        converter.setOption("tasklists", true);
        converter.setOption("tables", true);

        var str = self.text()
        self.html(converter.makeHtml(str))

        var code = self.find('pre code')
        code.each(function (i, block) {
            hljs.highlightBlock(block);
        });
    </script>
</div>
`
}

var bindEventTopicCommentAdd = function () {
    $(".btn-topic-comment-add").click(function () {
        var self = $(this)
        if (self.hasClass('disabled')) return false
        var comment = $('.input-topic-comment')

        var id = self.closest('.container').data('id')

        var form = {
            content: filterXSS(comment.val()),
            blog_id: id
        };

        var response = function (r) {
            if (r.success) {
                location.reload()
            } else {
                alert(r.message)
            }
        }
        api.commentTopic(id, form, response)
    })
}

var deleteTopic = function () {
    $('.btn-delete-topic').click(function () {
        return false
    })
}

var editTopic = function () {
    $('.btn-edit-blog').click(function () {
        var blog_id = $('.container').data('id')
        location.href = '/blog/edit/' + blog_id
    })
}

$(document).ready(function () {
    formatTimestamp()
    goTop()
    bindEventTopicCommentAdd()
    checkSubmit(".input-topic-comment", ".btn-topic-comment-add", 3)
})
