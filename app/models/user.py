from app.tools.enums import PendingStatus
from app.models.base import Base,db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.tools.helper import is_isbn_or_key

from flask import current_app
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
#Werkzeug 是一个 WSGI 工具包
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import login_manager
from app.spider.rec_book import RecBook
class User(Base,UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    gifts = relationship('Gift')

    _password = Column('password', String(100),nullable=False)
    #密码读取,方法当成属性用
    @property
    def password(self):
        return self._password

    #密码加密写入
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
    #密码解析
    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    #判断是否能添加为gift或wish
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        rec_book = RecBook()
        rec_book.search_by_isbn(isbn)
        if not rec_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        #两个表都找不到才可以添加
        if not gifting and not wishing:
            return True
        else:
            return False

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    #类名.方法名()调用,不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样
    ''''''
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid=data.get('id')
        with db.auto_commit():
            #update user set password=new_password where id = uid
            user=User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    def can_satisfied_wish(self):
        receive_counter = self.receive_counter
        send_counter = self.send_counter

        return True if receive_counter - send_counter <= 1   else False


#No user_loader has been installed for this LoginManager 错误
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))