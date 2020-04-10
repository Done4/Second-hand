from wtforms.validators import DataRequired as WTFDataRrequired


#重写默认的WTF DataRequired，实现自定义message
class DataRequired(WTFDataRrequired):
    #直接对实例进行调用 ,对象看成函数
    def __call__(self, form, field):
        if self.message is None:
            field_text = field.label.text
            self.message = field_text + '不能为空，请填写' + field_text
        super(DataRequired, self).__call__(form, field)

