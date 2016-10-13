from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from routes.black import black_list

from functools import wraps
import json

from models.user import User
from time import time


def api_response(status=False, data=None, message=None):
    r = dict(success=status,
             data=data,
             message=message)
    return json.dumps(r, ensure_ascii=False)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None:
            abort(404)
        if u.id != 1:
            u.unsafe += 1
            u.save()
            abort(404)
        return f(u, *args, **kwargs)

    return function


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('user.index'))
        if u.id in black_list:
            abort(404)
        return f(u, *args, **kwargs)

    return function


def anti_frequently(item, longtime, msg, user=None):
    if user is not None and user.id == 1:
        return True, ''
    if item is None:
        return True, ''
    if int(time()) - item.created_time < longtime:
        return False, api_response(message=msg)
    return True, ''


def anti_update(item, longtime, msg, user=None):
    if user is not None and user.id == 1:
        return True, ''
    if item.updated_time == item.created_time:
        return True, ''
    if int(time()) - item.updated_time < longtime:
        return False, api_response(message=msg)
    return True, ''
