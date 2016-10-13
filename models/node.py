from . import *


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', backref='board')
    content = db.Column(db.String(100))
    keywords = db.Column(db.String(100))
    permit = db.Column(db.String(100))
    master = db.Column(db.String(100))
    show_name = db.Column(db.String(100))

    def __init__(self, form):
        self.name = form.get('name', '')
        self.parent_id = form.get("parent_id", 0)
        self.content = form.get("content", '')
        self.keywords = form.get("keywords", '板块')
        self.master = form.get('master', '')
        self.permit = form.get("permit", '')
        self.show_name = form.get("show_name", '')

    def update(self, form):
        print('board.update, ', form)

    def save_node(self):
        if 11 > len(self.name) > 0:
            if Node.query.filter_by(name=self.name).first() is None:
                self.save()
                return True, self.response(), '添加成功'
            return False, None, '添加失败, 节点名已存在'
        return False, None, '添加失败, 节点名长度不在1-10'

    def delete_node(self):
        for t in self.topics:
            t.delete()
        child = Node.query.filter_by(parent_id=self.id)
        for i in child:
            i.delete_node()
        self.delete()
        return True, None, '删除成功'

    def response(self):
        if self.parent_id == 0:
            parent = '自身是父节点' + self.name
        else:
            parent = Node.query.filter_by(id=self.parent_id).first().name

        return {
            'name': self.name,
            'parent': parent,
            'id': self.id,
        }
