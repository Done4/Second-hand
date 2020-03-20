from wtforms import StringField, PasswordField, Form
from .base import DataRequired

class LoginForm(Form):
    name = StringField('用户名',validators=[DataRequired(message='用户名不可以为空，请输入你的账号')])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码')])