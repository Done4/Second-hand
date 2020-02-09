from . import web
from flask import render_template
from app.models.gift import Gift
from app.view_models.book import  BookViewModelSQL
from flask_login import login_required,current_user

@web.route('/')
def index():
    recent_gifts=Gift.recent()
    books =[BookViewModelSQL(gift.book) for gift in recent_gifts]
    return render_template('index.html',recent=books)

@web.route('/personal')
@login_required
def personal_center():
    return render_template('personal.html', user=current_user.summary)