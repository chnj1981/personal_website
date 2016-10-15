var commentTemplate = function (c) {
    return `
<div class="comment-item row">
    <div class="col-xs-1 u-avatar"><img src=${ c.avatar } class="img-l img-rounded"></div>
    <div class="col-xs-8 u-comment">
        <a href="${ '/user/profile/' + c.user_id }">${ c.nickname }</a>
        <p>${ c.comment }</p>
        <p class="timestamp">${ timestampProcess(c.created_time) }</p>
    </div>
</div>

`
}

var bindEventBlogCommentAdd = function () {
    $(".btn-blog-comment-add").click(function () {

        var self = $(this)
        if (self.hasClass('disabled')) return false
        var comment = self.prev()

        var id = self.closest('.container').data('id')

        var form = {
            comment: filterXSS(comment.val()),
            blog_id: id
        };

        var comment_cells = self.parent().next();

        var response = function (r) {
            if (r.success) {
                // comment_cells.prepend()
                var new_comment = commentTemplate(r.data)
                $(new_comment).hide().prependTo(comment_cells).slideDown('slow');
                //$(response).hide().prependTo($('.list-group')).fadeIn('slow');
                self.addClass('disabled')
                comment.val('')
            } else {
                alert(r.message)
            }
        }
        api.blogCommentAdd(form, response)
    })
}

var gradeCount = function () {
    $('.btn-grade').on('click', function () {
        var self = $(this)
        var cnt = self.children().text()

        var grade = 'a'
        if (self.hasClass('grade-c')) {
            grade = 'c'
        } else if (self.hasClass('grade-e')) {
            grade = 'e'
        }

        var form = {
            grade: grade,
            blog_id: $('.container').data('id')
        }

        var response = function (r) {
            if (r.success) {
                var update = parseInt(cnt) + 1
                self.children().text(update)
                alert(r.message)
            } else {
                alert(r.message)
            }
        }
        api.gradeCountAdd(form, response)
        return false
    })
}

var deleteBlog = function () {
    $('.btn-delete-blog').click(function () {
        var response = function (r) {
            if (r.success) {
                alert(r.message)
                location.href = '/blog'
            } else {
                alert(r.message)
            }
        }
        var blog_id = $('.container').data('id')
        api.deleteBlog(blog_id, response)
        return false
    })
}

var editBlog = function () {
    $('.btn-edit-blog').click(function () {
        var blog_id = $('.container').data('id')
        location.href = '/blog/edit/' + blog_id
    })

}

$(document).ready(function () {
    formatTimestamp()
    goTop()
    gradeCount()
    deleteBlog()
    editBlog()
    bindEventBlogCommentAdd()
    checkSubmit(".input-blog-comment", ".btn-blog-comment-add", 3)
})


