from app.spider.rec_book import RecBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean,desc,func
from sqlalchemy.orm import relationship
from app.models.base import Base,db


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        rec_book = RecBook()
        rec_book.search_by_isbn(self.isbn)
        return rec_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的isbn_list 到gift表中计算某个礼物心愿数量
        # 条件表达式
        # 分组查数量
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        # count_list=[EachGiftWishCount(w[0],w[1]) for w in count_list]
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


