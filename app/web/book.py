from sqlalchemy.exc import IntegrityError

from app.view_models.trade import TradeInfo
from flask import jsonify, request, json, render_template, flash, current_app
from flask_login import current_user
from app.libs.helper import is_isbn_or_key
from app.spider.rec_book import RecBook
from . import web
from app.forms.book import SearchForm
from app.view_models.book import BookCollection, BookViewModel, BookViewModelSQL
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from ..models.book import Book


@web.route('/book/search')
def search():
    '''
    q:普通关键字 isbn
    page
    '''
    #验证层
    form=SearchForm(request.args)
    books=BookCollection()

    if form.validate():
        q=form.q.data
        page =form.page.data
        isbn_or_key=is_isbn_or_key(q)
        rec_book = RecBook()

        if isbn_or_key =='isbn':
            f=rec_book.search_by_isbn(q)
        else:
            f=rec_book.search_by_keyword(q,page)

        books.fill(rec_book,q,f)
        if f=='api':
            save_book(books.books)
        #API , dict 序列化
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)

@web.route('/aa')
def he():
    flash('haha')
    return '你是傻逼'

@web.route('/book/<isbn>/detail')
# @cache.cached(timeout=1800)
def book_detail(isbn):
    """
        1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
        2. 当书籍在心愿清单时，显示礼物清单
        3. 当书籍在礼物清单时，显示心愿清单
        4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的

        这个视图函数不可以直接用cache缓存，因为不同的用户看到的视图不一样
        优化是一个逐步迭代的过程，建议在优化的初期，只缓存那些和用户无关的“公共数据"
    """
    has_in_gifts = False
    has_in_wishes = False

    #  获取图书信息
    rec_book = RecBook()
    f=rec_book.search_by_isbn(isbn)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True
    if f=='api':
        book = BookViewModel(rec_book.first)
    else:
        book = BookViewModelSQL(rec_book.first)
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)

def save_book(books):
    for b in books:
        try:
            book = Book()
            book.title = b.title
            book.author = b.author
            book.binding = b.binding
            book.publisher = b.publisher
            book.image = b.image
            book.price = b.price
            book.isbn = b.isbn
            book.pubdate = b.pubdate
            book.summary = b.summary
            book.pages = b.pages
            db.session.add(book)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.exception('%r' % e)


