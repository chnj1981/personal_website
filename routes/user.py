from routes import *

from models.user import User

main = Blueprint('user', __name__)


@main.route('/')
def index():
    if current_user() is None:
        return render_template('user_login.html', user=None)
    return redirect(url_for('weibo.index'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    ip = request.remote_addr
    user_id, msgs = u.valid_register(ip)
    if user_id is None:
        return api_response(message=msgs)
    session['user_id'] = u.id
    return api_response(True, {'id': user_id})


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.valid_login()
    if user_id is None:
        return api_response(message=msg)
    session['user_id'] = user_id
    return api_response(True, message=msg)


@main.route('/logout')
@login_required
def logout(user):
    session.pop('user_id', None)
    return redirect(url_for('.index'))


@main.route('/user/update_password', methods=['POST'])
@login_required
def update_password(user):
    return render_template('test_user.html')


@main.route('/user/profile_update', methods=['POST'])
@login_required
def profile_update(user):
    form = request.form
    id = int(form.get('id'))
    if id != user.id:
        return abort(404)
    status, data, msg = user.profile_update(form)
    return redirect(url_for('.index'))


@main.route('/user/profile/<int:id>')
@login_required
def profile(user, id):
    view_user = User.query.get_or_404(id)
    return render_template('profile.html', user=user, view_user=view_user)


@main.route('/taoing')
@login_required
def taoing(user):
    return render_template('taoing.html')


@main.route('/control')
@admin_required
def control(user):
    users = User.query.all()
    return render_template('control.html', users=users, user=user)
