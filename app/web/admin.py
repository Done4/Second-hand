from flask import render_template, request,url_for,redirect,flash

from . import web
from ..forms.admin import LoginForm
from ..models.admin import Admin


@web.route('/back', methods=['GET', 'POST'])
def back():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = Admin.query.filter_by(name=form.name.data).first()
        if admin and admin.check_password(form.password.data):
            return redirect(url_for('web.index'))
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('admin/login.html', form=form)

@web.route('/back/index')
def backindex():
    return render_template('admin/index.html')

@web.route('/back/admin')
def backadmin():
    return render_template('admin/admin_list.html')

@web.route('/back/user')
def backuser():
    return render_template('admin/user_list.html')

@web.route('/back/product')
def backproduct():
    return render_template('admin/product_list.html')