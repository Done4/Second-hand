
from . import web
from flask import render_template
from app.models.gift import Gift
from app.view_models.book import  BookViewModelSQL
from flask_login import login_required, current_user

from ..models.base import db
from ..models.book import Book
from ..tools.itemCF import ItemBasedCF


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books =[BookViewModelSQL(gift.book) for gift in recent_gifts]
    '''
    显示热门书
    统计 wish表未完成的书籍和drift表已完成和待完成的书籍 作为 热门书籍
    '''
    sql = 'select sum(ci),isbn ' \
          'from (' \
          '(select count(drift.isbn) as ci , isbn from drift ' \
          'where pending = 2 or pending = 1 group by isbn) union' \
          '(select count(wish.isbn), isbn from wish where ' \
          'launched = 0 group by isbn )' \
          ') as tall group by isbn order by ci desc limit 6'
    row = db.session.execute(sql)
    hotbooks = [Book.query.filter(Book.isbn == isbn[1]).all() for isbn in row.fetchall()]
    #判断用户是否登录,如有用户登录为他进行个性化推荐
    if current_user.is_authenticated:
        items = ItemBasedCF()
        result = items.recommend(current_user.id)
        #推荐结果不为空就替代热门书籍显示
        if result:
            hotbooks = [Book.query.filter(Book.isbn == r[0]).all() for r in result]
    return render_template('index.html', recent=books, hotbooks=hotbooks)

@web.route('/personal')
@login_required
def personal_center():
    return render_template('personal.html', user=current_user.summary)