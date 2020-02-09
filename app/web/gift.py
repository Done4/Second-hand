from . import web
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for, current_app
from app.models.base import db
from app.models.gift import Gift
from app.spider.rec_book import RecBook
from app.view_models.gift import MyGifts
from ..libs.enums import PendingStatus
from ..models.drift import Drift


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid=current_user.id
    gifts_of_mine=Gift.get_user_gifts(uid)
    isbn_list=[gift.isbn for gift in gifts_of_mine]
    wish_count_list=Gift.get_wish_counts(isbn_list)
    view_model=MyGifts(gifts_of_mine,wish_count_list)
    return render_template('my_gifts.html',gifts=view_model.gifts)

@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    rec_book = RecBook()
    rec_book.search_by_isbn(isbn)
    # gifting = Gift.query.filter_by(uid=current_user.id, isbn=isbn, status=1,
    #                                launched=False).first()
    # wishing = Wish.query.filter_by(uid=current_user.id, isbn=isbn, status=1,
    #                                launched=False).first()
    if current_user.can_save_to_list(isbn):
        # 既不在赠送清单，也不在心愿清单才能添加
        with db.auto_commit():
            #事务
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            # gift.book_id = yushu_book.data.id
            db.session.add(gift)
            #current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first()
    if not gift:
        flash('该书籍不存在，或已经交易，删除失败')
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往交易处理')
    else:
        with db.auto_commit():
            gift.delete()
    return redirect(url_for('web.my_gifts'))
