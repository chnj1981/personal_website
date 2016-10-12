from models.topic import Topic, TopicComment
from models.node import Node
from routes import *
from sqlalchemy import or_, and_

main = Blueprint('forum', __name__)

_Model = Topic
_Model2 = TopicComment


@main.route('/')
@login_required
def index(user):
    return redirect(url_for('.board', nodename='all'))


@main.route('/<nodename>/')
@login_required
def board(user, nodename):
    items_per_page = 15
    if nodename == 'all':
        page = request.args.get('page', 1, type=int)
        p = Topic.query.order_by(_Model.order_time.desc()).paginate(page, items_per_page,
                                                                    False)
        return render_template('forum_index.html', p=p, Node=Node, node=nodename,
                               user=user)

    n = Node.query.filter_by(name=nodename).first()
    child = Node.query.filter_by(parent_id=n.id).all()
    c = [i.id for i in child]
    c.append(n.id)
    page = request.args.get('page', 1, type=int)
    p = Topic.query.filter(_Model.board_id.in_(c)).order_by(
        _Model.order_time.desc()).paginate(page, items_per_page, False)
    return render_template('forum_index.html', p=p, Node=Node, node=nodename, user=user)


@main.route('/topic/<int:id>/')
@login_required
def show(user, id):
    m = _Model.query.get_or_404(id)
    m.views += 1
    m.save()
    return render_template('topic_content.html', t=m, user=user)


@main.route('/topic/edit/<id>/')
@login_required
def edit(user, id):
    m = _Model.query.get_or_404(id)
    return render_template('topic_edit.html', topic=m, Node=Node, user=user)


@main.route('/topic/update/<id>', methods=['POST'])
@login_required
def update(user, id):
    m = _Model.query.get_or_404(id)
    if m.user.id != user.id:
        return abort(404)
    status, resp = anti_update(m, 3600, '一小时内只能更新一次', user)
    if not status:
        return resp
    form = request.form
    status, data, msg = m.update(form)
    return api_response(status, data, msg)


@main.route('/topic/add', methods=['POST'])
@login_required
def add(user):
    ftp = user.topics.first()
    status, resp = anti_frequently(ftp, 600, '请间隔10分钟发帖', user)
    if not status:
        return resp

    form = request.form
    m = _Model(form)
    status, data, msg = m.add(user)
    return api_response(status, data, msg)


@main.route('/topic/comment/<int:id>', methods=['POST'])
@login_required
def comment(user, id):
    ftpc = user.topic_comments.first()
    status, resp = anti_frequently(ftpc, 30, '请间隔30秒评论', user)
    if not status:
        return resp
    topic = _Model.query.get_or_404(id)
    form = request.form
    m = _Model2(form)
    status, data, msg = m.add(user, topic)
    return api_response(status, data, msg)


@main.route('/topic/new')
@login_required
def new(user):
    return render_template('topic_edit.html', topic=None, Node=Node, user=user)


@main.route('/topic/delete/<int:id>')
@admin_required
def delete(user, id):
    t = _Model.query.get_or_404(id)
    t.delete()
    return redirect(url_for('.index'))
