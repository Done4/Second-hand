from . import web
from app.models.book import Book
from app.view_models.book import BookViewModel
@web.route('/test')
def ha():
    # s='w'
    # key='%'+s+'%'
    # b=Book.query.filter(Book.title.like(key))
    # print(b.count())
    # for i in b:
    #  print(i.title)
    b=Book.query.filter(Book.isbn == '9787121016653')
    print(b.count())
    for i in b:
        print(i.title)

    return '222'