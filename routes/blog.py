from routes import *

from models.blog import Blog, BlogComment

main = Blueprint('blog', __name__)

_MODEL = Blog
_MODEL2 = BlogComment


@main.route('/')
def index():
    user = current_user()
    models = _MODEL.all()
    return render_template('blog_index.html', blogs=models, user=user)


@main.route('/content/<int:id>')
def content(id):
    m = _MODEL.query.get_or_404(id)
    next = _MODEL.query.filter(_MODEL.id > id).first()
    prev = _MODEL.query.filter(_MODEL.id < id).order_by(_MODEL.id.desc()).first()
    return render_template('blog_content.html', b=m, user=user, next_one=next,
                           prev_one=prev)


@main.route('/comment/add', methods=['POST'])
@login_required
def comment(user):
    fbc = user.blog_comments.first()
    status, resp = anti_frequently(fbc, 30, '请间隔30秒评论', user)
    if not status:
        return resp

    form = request.form
    blog = _MODEL.query.get_or_404(form.get('blog_id'))
    m = _MODEL2(form)
    status, data, msg = m.save_comment(user, blog)
    return api_response(status, data, msg)


@main.route('/comment/grade', methods=['POST'])
@login_required
def grade(user):
    form = request.form
    ip = request.remote_addr
    m = _MODEL.query.get_or_404(form.get('blog_id'))
    status, data, msg = m.update_grade(form, ip)
    return api_response(status, data, msg)


@main.route('/new')
@admin_required
def new(user):
    return render_template('blog_edit.html', blog=None, user=user)


@main.route('/add', methods=['POST'])
@admin_required
def add(user):
    form = request.form
    status, data, msg = _MODEL(form).blog_add()
    return api_response(status, data, msg)


@main.route('/edit/<int:id>')
@admin_required
def edit(user, id):
    m = _MODEL.query.get_or_404(id)
    return render_template('blog_edit.html', blog=m, user=user)


@main.route('/update/<int:id>', methods=['POST'])
@admin_required
def update(user, id):
    m = _MODEL.query.get_or_404(id)
    status, data, msg = m.blog_update(request.form)
    return api_response(status, data, msg)


@main.route('/delete/<int:id>')
@admin_required
def delete(user, id):
    m = _MODEL.query.get_or_404(id)
    m.delete()
    return api_response(True, message='删除成功')
