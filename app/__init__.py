from flask import Flask

from flask_login import LoginManager
from app.models.base import db
from app.tools.email import mail
from flask_migrate import Migrate
import time

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    #导入配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    #注册蓝图
    register_web_blueprint(app)
    # 注册email模块
    mail.init_app(app)
    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 自定义过滤器
    # 时间格式化
    @app.template_filter("time_filter")
    def time_filter(time_stamp):
        time_array = time.localtime(time_stamp)
        return time.strftime('%Y-%m-%d %H:%M',time_array)

    db.init_app(app)
    with app.app_context():
        #db.drop_all()#删库重建
        db.create_all()


    #数据库迁移
    migrate = Migrate(app, db)
    return app

def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)



