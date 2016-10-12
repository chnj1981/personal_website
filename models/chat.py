import json
from sqlalchemy import desc
from . import ModelMixin
from . import db
from . import timestamp
from models.user import User


class Chat(db.Model, ModelMixin):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    channel = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.Integer)

    def __init__(self, form, user):
        self.content = form.get('content', '')
        self.channel = form.get('channel')
        self.user = user
        self.created_time = timestamp()

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

    def save_record(self, user):
        status, msg = self.valid()
        if status:
            self.user = user
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
