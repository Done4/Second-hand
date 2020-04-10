from . import web
from app.models.book import Book
from app.view_models.book import BookViewModel
from ..tools.itemCF import ItemBasedCF


@web.route('/test')
def ha():
    # s='w'
    # key='%'+s+'%'
    # b=Book.query.filter(Book.title.like(key))
    # print(b.count())
    # for i in b:
    #  print(i.title)
    b = Book.query.filter(Book.isbn == '9787121016653').all()
    print(b)
    for i in b:
        print(i.title)

    return '222'

@web.route('/test/itemcf')
def item():
    items = ItemBasedCF()
    rec = items.recommend('2')
    print('rec',[re[0] for re in rec])
    return '推荐成功'