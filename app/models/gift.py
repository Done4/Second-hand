from app.models.base import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from flask import  current_app
from app.spider.rec_book import RecBook
from app.models.base import db

from collections import namedtuple

#EachGiftWishCount=namedtuple('EachGiftWishCount',['count','isbn'])
class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False) #是否送出

    def is_yourself_gift(self,uid):
        return True if self.uid == uid else False
    @classmethod
    def get_user_gifts(cls,uid):
        gifts=Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.models.wish import Wish
        #根据传入的isbn_list 到wish表中计算某个礼物心愿数量
        #条件表达式
        #分组查数量
        count_list=db.session.query(func.count(Wish.id),Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),Wish.status==1).group_by(
            Wish.isbn).all()
        #count_list=[EachGiftWishCount(w[0],w[1]) for w in count_list]
        count_list=[{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list
    @classmethod
    def recent(cls):
        recent_gift=Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        rec_book=RecBook()
        rec_book.search_by_isbn(self.isbn)
        return rec_book.first


