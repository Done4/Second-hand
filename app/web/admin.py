from flask import render_template, request, url_for, redirect, flash,current_app

from . import web
from ..forms.admin import LoginForm
from ..forms.book import UploadForm
from ..models.admin import Admin
from ..models.base import db
from ..models.book import Book
from ..models.user import User
from werkzeug.utils import secure_filename
import os

@web.route('/back', methods=['GET', 'POST'])
def back():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        #select * from admin where name=form.name.data
        admin = Admin.query.filter_by(name=form.name.data).first()
        if admin and admin.check_password(form.password.data):
            return redirect(url_for('web.index'))
        else:
            flash('账号不存在或密码错误')
    return render_template('admin/login.html', form=form)

#后台主页,前端页面写登录拦截
@web.route('/back/index')
def backindex():
    return render_template('admin/index.html')

@web.route('/back/admin')
def backadmin():
    #select * from admin
    admins = Admin.query.all()
    return render_template('admin/admin_list.html',admins=admins)

@web.route('/back/user')
def backuser():
    #select * from user
    users = User.query.all()
    return render_template('admin/user_list.html',users=users)

@web.route('/back/product')
def backproduct():
    #select * from book
    books = Book.query.all()
    return render_template('admin/product_list.html',books=books)

#管理员

#用户

#封号
@web.route('/back/lock.user/<int:uid>')
def backlock(uid):
    #select * from user where id = uid and status = 1
    user = User.query.filter(User.id == uid, User.status == 1).first()
    if not user:
        flash('该用户已被注销或已被封号')
    else:
        with db.auto_commit():
            user.status=99
    return redirect(url_for('web.backuser'))
#解封账号
@web.route('/back/unlock.user/<int:uid>')
def backunlock(uid):
    #select * from user where id = uid and status = 99
    user = User.query.filter(User.id == uid, User.status == 99).first()
    if not user:
        flash('该用户没有被封号，无需解封。')
    else:
        with db.auto_commit():
            user.status=1
    return redirect(url_for('web.backuser'))
#注销账号
@web.route('/back/delete.user/<uid>')
def backdeleteuser(uid):
    # select * from user where id = uid and status = 1
    user = User.query.filter(User.id == uid , User.status == 1).first()
    if not user:
        flash('该用户已被注销或已被封号')
    else:
        with db.auto_commit():
            user.delete()
    return redirect(url_for('web.backuser'))
#书籍
#上传书籍
@web.route('/back/upload.product',methods=['GET','POST'])
def upload_file():
    form = UploadForm(request.form)
    file = request.files['file']
    if file.filename == '':
        flash('没有选择图片')
        return redirect(url_for('web.backproduct'))
    if allowed_file(file.filename) and form.validate():
        filename = secure_filename(file.filename)
        #把图片保存到本地
        file.save(os.path.join(current_app.config['FILE_FOLDER'], filename))
        #print(filename)
        with db.auto_commit():
          book = Book()
          #键值对赋值
          book.set_attrs(form.data)
          book.image='../static/img/'+filename
         # print(book)
          db.session.add(book)
    else:
        flash('上传文件不合标准')
    return redirect(url_for('web.backproduct'))

def allowed_file(filename):
    # 获取文件扩展名，以'.'为右分割然后取第二个值
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['jpg','png']

#交易