from app.tools.email import send_email
from app.models.gift import Gift
from app.models.wish import Wish
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from . import web
from app.spider.rec_book import RecBook
from app.models.base import db
from app.view_models.gift import MyGifts


@web.route('/my/wish')
@login_required
def my_wish():
    uid=current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    # 获取wish的ISBN列表
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    # 计算想送这本书的人数，返回人数 和 ISBN 的集合
    gift_count_list = Wish.get_gifts_counts(isbn_list)
    #gift 和 wish 的模板结构一样，复用gift的模板
    view_model = MyGifts(wishes_of_mine, gift_count_list)
    return render_template('my_wishes.html', wishes=view_model.gifts)

#将书籍添加至心愿清单
@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    # rec_book = RecBook()
    # rec_book.search_by_isbn(isbn)
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))

#发送请求邮件索要书籍
@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    #返回指定主键对应的行，如不存在，返回404
    wish = Wish.query.get_or_404(wid)
    #select * from gift where uid = id and isbn = wish.isbn and status = 1
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_email(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))

#撤销wish
@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    #select * from wish where isbn = isbn and launched = false and status = 1
    wish = Wish.query.filter_by(isbn=isbn,launched=False).first()
    if not wish:
        flash('该心愿不存在，删除失败')
    else:
        with db.auto_commit():
            wish.delete()
    return redirect(url_for('web.my_wish'))