import hashlib
import os
import re
from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    password = db.Column(db.String(15))
    nickname = db.Column(db.String(10))
    email = db.Column(db.String(80), default='')
    github = db.Column(db.String(50), default='')
    qq = db.Column(db.String(20), default='')
    avatar = db.Column(db.String(300),
                       default='http://img.doutula.com/production/uploads/image/2016/04'
                               '/28/20160428814398_VIibxX.gif')
    weibos = db.relationship('Weibo', backref='user', lazy='dynamic',
                             order_by="desc(Weibo.id)")
    chats = db.relationship('Chat', backref='user', lazy='dynamic')
    weibo_comments = db.relationship('Comment', backref='user', lazy='dynamic',
                                     order_by="desc(Comment.id)")
    blog_comments = db.relationship('BlogComment', backref='user', lazy='dynamic',
                                    order_by="desc(BlogComment.id)")
    topics = db.relationship('Topic', backref='user', lazy='dynamic',
                             order_by="desc(Topic.id)")
    topic_comments = db.relationship('TopicComment', backref='user', lazy='dynamic',
                                     order_by="desc(TopicComment.id)")
    like_weibo = db.Column(db.String(10000), default='')

    ip_register = db.Column(db.String(15), default='')
    unsafe = db.Column(db.Integer, default=0)

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.confirm = form.get('confirm', '')
        self.nickname = form.get('nickname', '')
        self.captcha = form.get('captcha', '')

    def valid_register(self, ip):
        ip_user = User.query.filter_by(ip_register=ip).first()
        if ip_user is not None and ip_user.id != 1:
            return None, '注册失败, 此IP已有注册用户, 如有需要, 请联系管理员'
        self.ip_register = ip
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_nickname = User.query.filter_by(nickname=self.nickname).first() == None
        valid_password = self.password == self.confirm
        valid_nickname_len = 10 >= len(self.nickname) >= 1
        valid_username_len = 15 >= len(self.username) >= 6
        valid_password_len = 15 >= len(self.password) >= 6
        valid_captcha = self.captcha == 'python'
        err_msgs = ''

        u_match = r'^[\w]{6,15}$'
        n_match = r'^[\u4e00-\u9fa5\w]{1,10}$'

        if (not re.match(u_match, self.username)):
            err_msgs += '用户名包含非法字符<br>'
        elif (not re.search('[^_]+', self.username)):
            err_msgs += '用户名不能全为下划线<br>'

        if (not re.match(u_match, self.password)):
            err_msgs += '密码包含非法字符<br>'
        elif (not re.search('[^_]+', self.password)):
            err_msgs += '密码不能全为下划线<br>'

        if (not re.match(n_match, self.nickname)):
            err_msgs += '昵称包含非法字符<br>'
        elif (not re.search('[^_]+', self.nickname)):
            err_msgs += '昵称不能全为下划线<br>'

        if not valid_password:
            err_msgs += '两次输入密码不相同<br>'
        if not valid_nickname:
            err_msgs += '昵称已经存在<br>'
        if not valid_nickname_len:
            err_msgs += '昵称长度不合法<br>'
        if not valid_username:
            err_msgs += '用户名已存在<br>'
        if not valid_username_len:
            err_msgs += '用户名长度不合法<br>'
        if not valid_password_len:
            err_msgs += '密码长度不合法<br>'
        if not valid_captcha:
            err_msgs += '邀请码错误<br>'
        if err_msgs == '':
            self.save()
            return self.id, '注册成功, 已经自动登录'
        err_msgs += '注册失败'
        return None, err_msgs

    def valid_login(self):
        err_msg = '登录失败, 用户名或密码错误'
        suc_msg = '登录成功'
        user = User.query.filter_by(username=self.username,
                                    password=self.password).first()
        if user is not None:
            return user.id, suc_msg
        return None, err_msg

    def change_avatar(self, avatar):
        self.avatar = avatar
        self.save()
        return True

    def profile_update(self, form):
        self.avatar = form.get('avatar', self.avatar)
        self.email = form.get('email', self.email)
        self.qq = form.get('qq', self.qq)
        self.github = form.get('github', '')

        self.save()
        return True, None, '更新成功'
