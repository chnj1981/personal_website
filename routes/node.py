from models.node import Node
from models.topic import Topic
from routes import *

main = Blueprint('node', __name__)

_Model = Node


@main.route('/')
@admin_required
def index(user):
    ms = _Model.query.filter_by(parent_id=0).all()
    return render_template('node_index.html', node_list=ms, Node=Node, user=user)


@main.route('/add', methods=['POST'])
@admin_required
def add(user):
    form = request.form
    m = _Model(form)
    status, data, msg = m.save_node()
    return api_response(status, data, msg)


@main.route('/delete/<int:id>')
@admin_required
def delete(user, id):
    t = _Model.query.get_or_404(id)
    status, data, msg = t.delete_node()
    return api_response(status, data, msg)
