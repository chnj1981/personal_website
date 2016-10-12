from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db

from models.user import User
from models.node import Node
from models.topic import Topic, TopicComment
from models.weibo import Weibo, Comment
from models.blog import Blog, BlogComment
from models.chat import Chat

from routes.node import main as routes_node
from routes.forum import main as routes_forum
from routes.user import main as routes_user
from routes.weibo import main as routes_weibo
from routes.blog import main as routes_blog
from routes.weibo_api import main as routes_weibo_api

# from routes.chat import main as routes_chat

app = Flask(__name__)
db_path = '.sqlite'
manager = Manager(app)


def register_routes(app):
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_node, url_prefix='/forum/node')
    app.register_blueprint(routes_forum, url_prefix='/forum')
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_weibo_api, url_prefix='/api/weibo')
    # app.register_blueprint(routes_chat, url_prefix='/chat')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = ''
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/'
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@manager.command
def server():
    app = configured_app()
    # config = dict(
    #     debug=True,
    #     host='0.0.0.0',
    #     port=3000,
    # )
    # app.run(**config)
    app.run()


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
