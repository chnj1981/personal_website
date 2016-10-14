from . import *


class TopicComment(db.Model, ModelMixin):
    __tablename__ = 'topic_comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.updated_time = timestamp()

    def valid(self):
        return 1000 > len(self.content) > 3

    def add(self, user, topic):
        if self.valid():
            self.user = user
            self.topic = topic
            self.save()
            topic.comments_num += 1
            topic.order_time = timestamp()
            topic.save()
            return True, self.response(), '评论成功'
        return False, None, '评论失败'

    def response(self):
        return {
            'id': self.id,
            'content': self.content,
            'topic_id': self.topic_id,
            'user_id': self.user_id,
            'nickname': self.user.nickname,
            'avatar': self.user.avatar,
            'created_time': self.created_time,
        }


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5000))
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    order_time = db.Column(db.Integer)
    views = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=0)

    comments_num = db.Column(db.Integer, default=0)
    comments = db.relationship('TopicComment', backref='topic',
                               order_by=lambda: TopicComment.id.desc())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.board_id = form.get('board_id', 0)
        self.created_time = timestamp()
        self.order_time = timestamp()
        self.updated_time = timestamp()

    def update(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = timestamp()
        if self.valid():
            self.save()
            return True, self.response(), '更新成功'
        return False, None, '更新失败, 标题1-100字, 内容 20-5000字, 请仔细检查格式'

    def valid(self):
        return 0 < len(self.title) < 100 and 20 < len(self.content) < 5000

    def add(self, user):
        if self.valid():
            self.user = user
            self.save()
            return True, self.response(), '成功发布帖子'
        return False, None, '帖子格式不合法, 标题1-100字, 内容 20-5000字, 请仔细检查格式'

    def response(self):
        return {
            'id': self.id
        }
