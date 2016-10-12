import json
from sqlalchemy import desc
from . import ModelMixin
from . import db
from . import timestamp
from models.user import User


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.Integer)
    comments = db.relationship(
        'Comment',
        backref='weibo',
        lazy='dynamic',
        order_by=lambda: Comment.created_time.desc()
    )
    comments_num = db.Column(db.Integer)
    like_nums = db.Column(db.Integer, default=0)
    updated_time = db.Column(db.Integer)

    def __init__(self, form):
        self.weibo = form.get('weibo', '')
        self.created_time = timestamp()
        self.updated_time = timestamp()
        self.comments_num = len(self.comments.all())

    def like(self, user):
        u_likes = user.like_weibo.split(';')
        if str(self.id) in u_likes:
            self.like_nums -= 1
            u_likes.remove(str(self.id))
            user.like_weibo = ';'.join(u_likes)
            user.save()
            return True, {'like_nums': self.like_nums}, '赞 - 1'
        user.like_weibo += (str(self.id) + ';')
        self.like_nums += 1
        self.save()
        return True, {'like_nums': self.like_nums}, '赞 + 1'

    def valid(self, update_weibo=None):
        if update_weibo is None:
            w = self.weibo.strip()
        else:
            w = update_weibo.strip()
        l = len(w)
        if l <= 2:
            return False, '微博太短了，不能少于 3 个字符'
        elif l > 255:
            return False, '微博太长了，不能超过 255 个字符'
        return True, '微博内容合法'

    def save_weibo(self, user):
        status, msg = self.valid()
        if status:
            self.user = user
            self.save()
            data = self.response()
        else:
            data = None
        return status, data, msg

    def delete_weibo(self):
        for i in self.comments:
            i.delete()
        self.delete()
        data = self.response()
        status = True
        msg = '微博删除成功'
        return status, data, msg

    def update(self, form):
        new = form.get('content')
        status, msg = self.valid(new)
        if status:
            self.weibo = new
            self.updated_time = timestamp()
            self.save()
            data = self.response()
        else:
            data = None
        return status, data, msg

    def response(self):
        return dict(
            id=self.id,
            weibo=self.weibo,
            nickname=self.user.nickname,
            created_time=self.created_time,
            avatar=self.user.avatar,
            comments_num=self.comments_num
        )


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.comment = form.get('comment', '')
        self.weibo_id = form.get('weibo_id', '')
        self.created_time = timestamp()

    def valid(self):
        w = self.comment.strip()
        l = len(w)
        if l < 3:
            return False, '评论太短了，不能少于 3 个字符'
        elif l > 100:
            return False, '评论太长了，不能超过 255 个字符'
        return True, '评论内容合法'

    def save_comment(self, user, weibo):
        status, msg = self.valid()
        if status:
            self.user = user
            self.weibo = weibo
            self.weibo.comments_num += 1
            self.save()
            data = self.response()
        else:
            data = None
        return status, data, msg

    def response(self):
        return dict(comment=self.comment,
                    nickname=self.user.nickname,
                    created_time=self.created_time,
                    avatar=self.user.avatar)
