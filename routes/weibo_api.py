from routes import *

import json

from models.weibo import Weibo, Comment
import time

main = Blueprint('api', __name__)

_MODEL = Weibo
_MODEL2 = Comment


@main.route('/add', methods=['POST'])
@login_required
def add(user):
    fwb = user.weibos.first()
    status, resp = anti_frequently(fwb, 60, '请间隔60秒发言', user=user)
    if not status:
        return resp

    form = request.form
    m = _MODEL(form)
    status, data, msg = m.save_weibo(user)
    return api_response(status, data, msg)


@main.route('/delete/<int:id>')
@admin_required
def delete(user, id):
    m = _MODEL.query.get_or_404(id)
    if m.user.id != user.id and user.id != 1:
        return abort(404)
    status, data, msg = m.delete_weibo()
    return api_response(status, data, msg)


@main.route('/comment/add', methods=['POST'])
@login_required
def add_comment(user):
    fwc = user.weibo_comments.first()
    status, resp = anti_frequently(fwc, 15, '请间隔15秒评论', user=user)
    if not status:
        return resp
    form = request.form
    weibo = _MODEL.query.get_or_404(form.get('weibo_id'))
    m = _MODEL2(form)
    status, data, msg = m.save_comment(user, weibo)
    return api_response(status, data, msg)


@main.route('/update', methods=['POST'])
@login_required
def update(user):
    form = request.form
    m = _MODEL.query.get_or_404(form.get('weibo_id'))
    if m.user.id != user.id and user.id != 1:
        return abort(404)
    status, resp = anti_update(m, 3600, '一小时内只能更新一次', user=user)
    if not status:
        return resp
    status, data, msg = m.update(form)
    return api_response(status, data, msg)


@main.route('/like/<int:id>')
@login_required
def like(user, id):
    m = _MODEL.query.get_or_404(id)
    status, data, msg = m.like(user)
    return api_response(status, data, msg)
