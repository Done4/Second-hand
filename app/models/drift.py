from app.tools.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    id = Column(Integer, primary_key=True)
    #邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
   #书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(200))
    book_img = Column(String(50))
    gift_id = Column(Integer)
    #请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    #赠送者信息
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))

    #交易状态
    _pending = Column('pending', SmallInteger, default=1)


    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
