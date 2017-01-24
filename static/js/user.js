var error_view = function (parent) {
    parent.removeClass('flipInY')
    parent.removeClass('bounceInDown')
    parent.addClass('shake')
    newone = parent.clone(true);
    parent.before(newone);
    parent.remove();
    invalidLogin()
    invalidRegister()
}

var successView = function (p) {
    p.parent().addClass('animated bounceOutUp')
}

var registerCheck = function (data) {
    var msgs = ''
    var u_match = /^[\w]{6,15}$/
    var p_match = /^[\w]{6,15}$/
    var n_match = /^[\u4e00-\u9fa5\w]{1,10}$/

    if (!u_match.test(data.username)) {
        msgs += '用户名不合法, 包含非法字符<br>       '
    } else if (!/[^_]+/.test(data.username)) {
        msgs += '用户名不合法, 不能全为下划线<br>'
    }

    if (data.password != data.confirm) {
        msgs += '两次输入的密码不相同<br>'
    }

    if (!p_match.test(data.password)) {
        msgs += '密码不合法, 包含非法字符<br>'
    } else if (!/[^_]+/.test(data.password)) {
        msgs += '密码不合法, 不能全为下划线<br>'
    }

    if (!n_match.test(data.nickname)) {
        msgs += '昵称不合法, 包含非法字符<br>'
    } else if (!/[^_]+/.test(data.nickname)) {
        msgs += '昵称不合法, 不能全为下划线<br>'
    }

    return msgs
}

var bindEventRegister = function () {
    $('.btn-register').click(function () {
        if ($(this).hasClass('disabled')) {
            return false
        }

        var parent = $(this).parents('.register')

        $('.register-empty').addClass('hide')
        $('.register-error').addClass('hide')

        var data = {
            username: parent.find(':input.username').val(),
            password: parent.find(':input.password').val(),
            confirm: parent.find(':input.confirm').val(),
            nickname: parent.find(':input.nickname').val(),
            captcha: parent.find(':input.captcha').val()
        }

        msgs = registerCheck(data)
        if (msgs != '') {
            error_view(parent)
            $('.register-empty').html(msgs)
            $('.register-empty').removeClass('hide')
            return false
        }

        var response = function (r) {
            if (r.success) {
                successView(parent);
                location.href = "/weibo"
            } else {
                $('.register-error').removeClass('hide');
                $('.register-error').html(r.message);
                error_view(parent)
            }
        };
        api.userRegister(data, response)
    })
};

var bindEventConvert = function () {
    $('.btn-change').click(function () {
        var login = $('.btn-login');
        var signin = $('.btn-register');
        login.addClass('disabled');
        signin.addClass('disabled');

        var parent = $(this).parents('.col-center-block');
        parent.addClass('hide');
        var sibling = parent.siblings('.col-center-block');
        sibling.removeClass('hide');
        sibling.addClass('flipInY')
    })
};


var bindEventLogin = function () {
    $('.btn-login').on('click', function () {
        if ($(this).hasClass('disabled')) {
            return false
        }
        var parent = $(this).parents('.login');

        $('.login-error').addClass('hide');

        var data = {
            username: parent.find(':input.username').val(),
            password: parent.find(':input.password').val()
        };

        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.container'));
                window.location.href = '/weibo'
            } else {
                $('.login-error').removeClass('hide');
                error_view(parent)
            }
        }

        api.userLogin(data, response)

    })
}


var bindFastLogin = function () {
    $('.btn-login-fast').on('click', function () {
        var parent = $(this).parents('.login');
        $('.login-error').addClass('hide');

        var data = {
            username: '123456',
            password: '123456'
        };

        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.container'));
                window.location.href = '/weibo'
            } else {
                $('.login-error').removeClass('hide');
                error_view(parent)
            }
        }

        api.userLogin(data, response)

    })
}


var bindEventJoke = function () {
    $('.btn-admin').click(function () {
        if ($(this).hasClass('disabled')) {
            return false
        }

        var parent = $(this).parents('.register')

        $('span.register-error').addClass('hide')

        captcha = parent.find(':input.captcha').val()

        if (captcha != 'heheadmin') {
            error_view(parent)
            $('.register-empty').removeClass('hide')
            $('.register-empty').text('验证码错误')
            return false
        }

        successView(parent)

        setTimeout('alertify.alert("你的管理员账号申请已通过审核, 欢迎你, 250号管理员, 请点击确认, 稍后页面将自动跳转")', 1500);

        setTimeout(function () {
            $('.container').remove()
            $('.joke').removeClass('hide')
            $('.joke').addClass('animated bounceInUp')
        }, 15000)
    })
}

var invalidRegister = function () {
    var username = $('.register :input.username')
    var password = $('.register :input.password')
    var confirm = $('.register :input.confirm')
    var nickname = $('.register :input.nickname')
    var captcha = $('.register :input.captcha')

    $('.register :input').keyup(function () {
        var u_valid = $.trim(username.val()).length > 5
        var p_valid = $.trim(password.val()).length > 5
        var cf_valid = $.trim(confirm.val()).length > 5
        var n_valid = $.trim(nickname.val()).length > 0
        var ca_valid = $.trim(captcha.val()).length > 0
        var pc_valid = $.trim(password.val()).length == $.trim(confirm.val()).length

        var b = $('.btn-register, .btn-admin')

        if (u_valid && p_valid && cf_valid && n_valid && ca_valid && pc_valid) {
            b.removeClass("disabled");

        } else {
            b.addClass("disabled");
        }
    })
}

var invalidLogin = function () {
    var username = $('.login :input.username')
    var password = $('.login :input.password')
    $('.login :input').keyup(function () {
        var u_valid = $.trim(username.val()).length > 5
        var p_valid = $.trim(password.val()).length > 5
        var b = $('.btn-login')

        if (u_valid && p_valid) {
            b.removeClass("disabled");

        } else {
            b.addClass("disabled");
        }
    })
}

var bindEvents = function () {
    bindFastLogin()
    bindEventLogin()
    bindEventConvert()
    bindEventRegister()
    // bindEventJoke()
    invalidLogin()
    invalidRegister()
    $(document).keypress(function (e) {
        if (e.which == 13) {
            $('.btn-login, .btn-register').click()
        }
    });
}

$(document).ready(function () {
    bindEvents()
})
