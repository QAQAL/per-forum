from flask import Flask
from config import secret_key
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.admin import main as admin_routes
from routes.mail import main as mail_routes


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便设置什么内容都可以
    app.secret_key = secret_key
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(mail_routes, url_prefix='/mail')

    return app

# 运行代码
if __name__ == '__main__':
    # debug 模式自动加载对代码的变动, 所以不用重启程序
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
        threaded=True,
    )
    app = configured_app()
    app.run(**config)
