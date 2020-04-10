DEBUG=True
JSON_AS_ASCII=False
#数据库
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI='mysql+cymysql://root:123@localhost:3306/rcbook'
SECRET_KEY = '\xe8\xbf\x99\xe5\xb0\xb1\xe6\x98\xaf\xe6\xaf\x95\xe8\xae\xbe\xe5\xaf\x86\xe7\xa0\x81'
# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '864051684@qq.com'
MAIL_PASSWORD = 'wtdfjtttxxgbbbea'

#上传文件
FILE_FOLDER = 'E:\\python代码\\project\\flask\\book\\app\\static\\img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
