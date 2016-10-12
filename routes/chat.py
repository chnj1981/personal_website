# import flask
# from flask import request
# import redis
# import time
# import json
# from . import *
# from models.chat import Chat
#
# '''
# cat 用来查看文件的linux命令,
# cat xxx.py
# head xxx.py -n 20 显示20行
#
#
# apt-get install redis-server
# pip3 install gunicorn python-redis
#
# git clone
# git pull
# '''
#
# '''
# # 使用 gunicorn 启动
# gunicorn --worker-class=gevent -t 9999 redischat:app -b 0.0.0.0:8000
# # 开启 debug 输出
# gunicorn --log-level debug --worker-class=gevent -t 999 redis_chat81:app
# # 把 gunicorn 输出写入到 gunicorn.log 文件中
# gunicorn --log-level debug --access-logfile gunicorn.log --worker-class=gevent -t 999
#  redis_chat81:app
# '''
#
# '''
# history|grep gunicorn
# nohup gunicorn --worker-class=gevent -t 9999 redischat:app -b 0.0.0.0:8000 &
# '''
#
# # 连接上本机的 redis 服务器
# # 所以要先打开 redis 服务器
# red = redis.Redis(host='localhost', port=6379, db=0)
# print('redis', red)
#
# # app = flask.Flask(__name__)
# # app.secret_key = 'key'
#
# # 发布聊天广播的 redis 频道
# chat_channel = 'chat'
#
# main = Blueprint('chat', __name__)
#
# _MODEL = Chat
#
#
# def stream():
#     '''
#     监听 redis 广播并 sse 到客户端
#     '''
#     # 对每一个用户 创建一个[发布订阅]对象
#     pubsub = red.pubsub()
#     # 订阅广播频道
#     pubsub.subscribe(chat_channel)
#     # 监听订阅的广播
#     for message in pubsub.listen():
#         print(message)
#         if message['type'] == 'message':
#             data = message['data'].decode('utf-8')
#             # 用 sse 返回给前端
#             yield 'data: {}\n\n'.format(data)
#
#
# @main.route('/subscribe')
# def subscribe():
#     print('into subcribe')
#     return Response(stream(), mimetype="text/event-stream")
#
#
# @main.route('/')
# def index():
#     return render_template('chat.html')
#
#
# def current_time():
#     return int(time.time())
#
#
# @main.route('/add', methods=['POST'])
# @login_required
# def add(user):
#     msg = request.get_json()
#     content = msg.get('content', '')
#     channel = msg.get('channel', '')
#     nickname = user.nickname
#     r = {
#         'name': nickname,
#         'content': content,
#         'channel': channel,
#         'created_time': (),
#     }
#     _MODEL(r, user).save()
#     message = json.dumps(r, ensure_ascii=False)
#     print('debug', message)
#     # 用 redis 发布消息
#     red.publish(chat_channel, message)
#     return 'OK'
#
#
# # if __name__ == '__main__':
# #     config = dict(
# #         debug=True,
# #     )
# #     app.run(**config)
