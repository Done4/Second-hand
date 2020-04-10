from flask import render_template, redirect
from flask import request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user


from . import web
from app.forms.auth import RegisterForm, LoginForm, ResetPasswordForm, EmailForm, \
    ChangePasswordForm
from app.models.user import User
from app.models.base import db
from app.tools.email import send_email

#用户注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
          user = User()
          user.set_attrs(form.data)
          db.session.add(user)
        #注册完自动登录
        login_user(user)
        return redirect(url_for('web.index'))
    return render_template('auth/register.html', form=form)


#用户登录
@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        #SELECT * FROM user WHERE email = %s AND status = 1
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            #记住登录,默认不记住 remember
            login_user(user)
            next = request.args.get('next')
            #防止重定向攻击 login?next=www.baidu.com
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)

#忘记密码，发送邮件修改
@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            #select * from user where email = account_email and status = 1
            user = User.query.filter_by(email=account_email).first_or_404()
            send_email(form.email.data, '重置你的密码',
                       'email/reset_password.html', user=user,
                       token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
    return render_template('auth/forget_password_request.html')

#忘记密码，修改密码后重定向回登录页面
@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('web.index'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        result = User.reset_password(token, form.password1.data)
        if result:
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            return redirect(url_for('web.index'))
    return render_template('auth/forget_password.html')

#修改密码，修改后重定向回个人信息页面
@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        #update user set password=new_password1.data where id = uid
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码已更新成功')
        return redirect(url_for('web.personal_center'))
    return render_template('auth/change_password.html', form=form)
    pass


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))

