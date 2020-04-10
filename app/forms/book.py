from wtforms import Form,StringField,IntegerField,BooleanField
from wtforms.validators import Length,NumberRange,Regexp
from flask_wtf.file import FileField,FileAllowed,FileRequired
from .base import DataRequired
#所有验证对象
class SearchForm(Form):
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    page = IntegerField(validators=[NumberRange(min=1,max=99)],default=1)

class DriftForm(Form):
    recipient_name = StringField(
        '收件人姓名', validators=[DataRequired(), Length(min=2, max=20,
                                                    message='收件人姓名长度必须在2到20个字符之间')])
    mobile = StringField('手机号', validators=[DataRequired(),
                                            Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField('留言')

    address = StringField(
            '邮寄地址', validators=[DataRequired(),
                                Length(min=10, max=70, message='地址还不到10个字吗？尽量写详细一些吧')])

class UploadForm(Form):
    #file = FileField(u'上传文件',validators=[FileRequired()])
    pages = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
    title = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    author = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    binding = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    publisher = StringField(validators=[DataRequired(),Length(min=1,max=50)])
    price = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    pubdate = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    isbn = StringField(validators=[DataRequired(),Length(min=1,max=15)])
    summary = StringField(validators=[DataRequired(),Length(min=1,max=3000)])
#18110064138 猿辅导 杨
