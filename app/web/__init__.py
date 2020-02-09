from flask import Blueprint,render_template
#蓝图层
web=Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):
    #AOP 思想
    return render_template('404.html'),404

#模块导入只能放下面
from app.web import auth
from app.web import main
from app.web import book
from app.web import errors
from app.web import wish
from app.web import gift
from app.web import drift
from app.web import passenger
from app.web import test