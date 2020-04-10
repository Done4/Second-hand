from wtforms import StringField, PasswordField, Form
from wtforms.validators import Length, Email, ValidationError, EqualTo
from .base import DataRequired
from app.models.user import User


class EmailForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
                                            Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])


class ChangePasswordForm(Form):
    old_password = PasswordField('原有密码', validators=[DataRequired()])
    new_password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField('确认新密码字段', validators=[DataRequired()])

#没有用自定义的datarequired
class LoginForm(EmailForm):
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请填写你的密码')])

class RegisterForm(EmailForm):
    nickname = StringField('昵称', validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间')])
    #自定义验证器 - namefield验证器
    # 在校验类内部函数的名字规则是固定的validate_属性名（这样wtforms才会自动识别）
    # 这样定义的格式，无需在validators中再次添加！
    # 这里只能有一个参数field,因为是在自己类内部，如果添加form参数会报错！
    def validate_email(self, field):
        #select * from user where email=email
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')
