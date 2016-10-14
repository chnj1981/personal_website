var api = {}

api.ajax = function (url, method, form, callback) {
    var request = {
        url: url,
        type: method,
        data: form,
        success: function (response) {
            var r = JSON.parse(response)
            callback(r)
        },
        error: function (response) {
            var r = {
                'success': false,
                message: '网络错误'
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.get = function (url, response) {
    api.ajax(url, 'get', {}, response)
}

api.post = function (url, form, response) {
    api.ajax(url, 'post', form, response)
}

api.weiboAdd = function (form, response) {
    var url = '/api/weibo/add'
    api.post(url, form, response)
}

api.weiboCommentAdd = function (form, response) {
    var url = '/api/weibo/comment/add'
    api.post(url, form, response)
}

api.weiboDelete = function (weiboId, response) {
    var url = '/api/weibo/delete/' + weiboId
    api.get(url, response)
}

api.weiboUpdate = function (form, response) {
    var url = '/api/weibo/update'
    api.post(url, form, response)
}

api.userLogin = function (form, response) {
    var url = '/login'
    api.post(url, form, response)
}

api.userRegister = function (form, response) {
    var url = '/register'
    api.post(url, form, response)
}

api.blogCommentAdd = function (form, response) {
    var url = '/blog/comment/add'
    api.post(url, form, response)

}

api.gradeCountAdd = function (form, response) {
    var url = '/blog/comment/grade'
    api.post(url, form, response)
}

api.addBlog = function (form, response) {
    var url = '/blog/add'
    api.post(url, form, response)
}

api.updateBlog = function (id, form, response) {
    var url = '/blog/update/' + id
    api.post(url, form, response)
}

api.deleteBlog = function (blog_id, response) {
    var url = '/blog/delete/' + blog_id
    api.get(url, response)
}

api.addNode = function (form, response) {
    var url = '/forum/node/add'
    api.post(url, form, response)
}

api.deleteNode = function (node_id, response) {
    var url = '/forum/node/delete/' + node_id
    api.get(url, response)
}

api.addTopic = function (form, response) {
    var url = '/forum/topic/add'
    api.post(url, form, response)
}

api.updateTopic = function (topic_id, form, response) {
    var url = '/forum/topic/update/' + topic_id
    api.post(url, form, response)
}

api.commentTopic = function (topic_id, form, response) {
    var url = '/forum/topic/comment/' + topic_id
    api.post(url, form, response)
}

api.weiboLike = function (weiboId, response) {
    var url = '/api/weibo/like/' + weiboId
    api.get(url, response)
}
