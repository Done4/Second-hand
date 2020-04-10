from app.models.base import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from flask import current_app
from app.spider.rec_book import RecBook
from app.models.base import db

class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False) #是否送出

    #判断当前id 和 gift id 是否相等，相等则是自己
    def is_yourself_gift(self,uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls,uid):
        # select  * from gift where uid = uid and launched = False and status = 1 order by create_time desc
        gifts = Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.models.wish import Wish
        #根据传入的isbn_list 到wish表中计算某个礼物心愿数量
        #select count(id),isbn from wish where launched = false and isbn in (9787540213206,1) and status = 1 group by isbn
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list), Wish.status == 1).group_by(
            Wish.isbn).all()
        #封装成字典列表返回
        count_list=[{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list
    #最近上传
    @classmethod
    def recent(cls):
        #group by 比order by先执行
        #select  * from gift where launched = false and status=1 group by isbn order by create_time desc limit 10
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gift

    @property
    def book(self):
        rec_book = RecBook()
        rec_book.search_by_isbn(self.isbn)
        return rec_book.first


