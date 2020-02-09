from flask import Flask

from flask_login import LoginManager
from app.models.base import db
from app.libs.email import mail
from flask_migrate import Migrate

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
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