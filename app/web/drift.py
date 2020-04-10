
from flask_login import login_required, current_user
from . import web
from flask import flash, redirect, url_for, render_template, request
from app.models.gift import Gift
from app.forms.book import DriftForm
from app.models.base import db
from app.models.drift import Drift
from app.view_models.book import  BookViewModelSQL
from app.tools.email import send_email
from sqlalchemy import desc,or_

from app.view_models.drift import  DriftCollection
from ..tools.enums import PendingStatus
from ..models.wish import Wish
from app.models.user import User
from app.models.book import Book

#发送请求邮件
@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的^_^, 不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    #限制无限索取，索求两本需要送出一本
    if not current_user.can_satisfied_wish():
        flash('每获取到两本书以后需要送出一本才可以继续索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    gifter = current_gift.user
    #获取书籍名字
    book_name = Book.query.filter_by(isbn=current_gift.isbn).first().title
    form = DriftForm(request.form)
    if request.method =='POST' and form.validate():
        save_drift(form,current_gift)
        send_email(current_gift.user.email, '有人想要《'+book_name+'》', 'email/get_gift.html',
                   wisher=current_user,
                   gift=current_gift)
        return redirect(url_for('web.index'))
    return render_template('drift.html', gifter=gifter, form=form, book_name=book_name)

#交易记录
@web.route('/pending')
@login_required
def pending():
    #select * from drift where requester_id = uid or gifter_id = uid order by create_time desc
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    view_model = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=view_model.data)

#拒绝请求，只有书籍赠送者才能拒绝请求
@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        # select * from drift where gifter_id = uid and id = did and status = 1
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        # update drift set pending = 3 where gifter_id = uid and id = did and status = 1
        drift.pending = PendingStatus.Reject
    return redirect(url_for('web.pending'))

#撤销请求，只有书籍请求者才可以撤销请求
@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        # 如果不加入这个条件，那么drift_id可能被修改
        #select * from drift where request_id = uid and id = did and status = 1
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        #update drift set pending = 4 where request_id = uid and id = did and status = 1
        drift.pending = PendingStatus.Redraw
    return redirect(url_for('web.pending'))


#邮寄书籍，只有书籍赠送者才能邮寄
@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        #select * from drift where gifter_id = uid and id = did and status = 1
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        # update drift set pending = 2 where gifter_id = uid and id = did and status = 1
        drift.pending = PendingStatus.Success
        # 赠送数量变化
        gifter = User.query.filter_by(id=drift.gifter_id).first_or_404()
        gifter.send_counter += 1
        # 接收数量变化
        receiver = User.query.filter_by(id=drift.requester_id).first_or_404()
        receiver.receive_counter += 1
        #改变书籍状态
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 不查询直接更新;这一步可以异步来操作 两种写法
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})

    return redirect(url_for('web.pending'))


def save_drift(drift_form,current_gift):
    with db.auto_commit():
        drift=Drift()
        drift_form.populate_obj(drift) #表单信息复制drift模型 ， 字段名字需对应

        drift.gift_id=current_gift.id
        drift.requester_id=current_user.id
        drift.gifter_nickname=current_gift.user.nickname
        drift.requester_nickname=current_user.nickname
        drift.gifter_id=current_gift.user.id
        #将字典转化成 对象
        book=BookViewModelSQL(current_gift.book)
        drift.book_title=book.title
        drift.book_author=book.author
        drift.book_img=book.image
        drift.isbn=book.isbn
        db.session.add(drift)
        book_name=drift.book_title
    return book_name