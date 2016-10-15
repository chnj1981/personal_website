import json
from sqlalchemy import desc
from . import ModelMixin
from . import db
from . import timestamp


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))
    title = db.Column(db.String(100))
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    grade_a = db.Column(db.Integer, default=0)
    grade_c = db.Column(db.Integer, default=0)
    grade_e = db.Column(db.Integer, default=0)
    ip = db.Column(db.String(10000), default='')
    comments = db.relationship(
        'BlogComment',
        backref='blog',
        lazy='dynamic',
        order_by=lambda: BlogComment.id.desc()
    )

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = timestamp()

    def valid(self):
        return len(self.title) > 0 and len(self.content) > 0

    def blog_add(self):
        if self.valid():
            self.save()
            return True, self.title, '添加博客成功'
        return False, None, '添加博客失败'

    def blog_update(self, form):
        title = form.get('title')
        content = form.get('content')
        msg = ''
        if self.title != title:
            self.title = title
        else:
            msg += '博客标题未变'
        if self.content != content:
            self.content = content
        else:
            msg += '博客内容未变'
        self.save()
        return True, self.title, msg

    def update_grade(self, form, ip):
        grade = form.get('grade')

        if ip in self.ip.split(';'):
            if grade == 'a':
                msg = '你想多赞几次? 只要你求我, 我还是愿意修改数据库的. 不要告诉我其实你刚错手踩了我...'
            else:
                msg = '这才是真实的评价么, 原来你错手点了个赞? 然而你已经没有第二次机会了, 啊哈哈哈哈哈! 不要告诉我其实你想多踩几次...'
            return False, None, msg

        if grade == 'a':
            self.grade_a += 1
        elif grade == 'c':
            self.grade_c += 1
        elif grade == 'e':
            self.grade_e += 1
        else:
            return False

        self.ip += (ip + ';')
        msg = {
            'a': '谢谢你的鼓励, 我会继续加油的! PS:这是匿名评价',
            'c': '感谢你的反馈, u can u up! PS:这是匿名评价',
            'e': '感谢你的反馈, 我会争取写出更烂的! PS:这是匿名评价',
        }.get(grade)
        self.save()
        return True, None, msg


class BlogComment(db.Model, ModelMixin):
    __tablename__ = 'blog_comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.Integer)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def __init__(self, form):
        self.comment = form.get('comment', '')
        self.created_time = timestamp()

    def valid(self):
        return 200 >= len(self.comment) >= 3

    def save_comment(self, user, blog):

        if self.valid():

            self.blog = blog
            self.user = user
            self.save()
            return True, self.response(), '添加博客评论成功'
        return False, None, '添加博客评论失败'

    def response(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'comment': self.comment,
            'created_time': self.created_time,
            'avatar': self.user.avatar,
            'nickname': self.user.nickname,
        }
