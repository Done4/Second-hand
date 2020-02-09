from app.libs.httper import HTTP
from flask import current_app
from app.models.book import Book
from app.view_models.book import BookCollection


class RecBook:
    per_page=15
    isbn_url='http://t.yushu.im/v2/book/isbn/{}'
    keyword_url='http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total=0
        self.books=[]

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def __fill_mysql(self,data,count):
        self.total=count
        self.books=data

    def __fill_mysql_single(self,data):
        if data:
            self.total = 1
            self.books=data

    def search_by_isbn(self,isbn):
        result=Book.query.filter(Book.isbn == isbn)
        count=result.count()
        if count == 0:
            url=self.isbn_url.format(isbn)
            result=HTTP.get(url)
            self.__fill_single(result)
            return 'api'
        else:
            self.__fill_mysql_single(result)
            return 'mysql'

    def search_by_keyword(self,keyword,page=1):

        key = '%' + keyword + '%'
        result=Book.query.filter(Book.title.like(key))
        count=result.count()
        if count > 0:
            self.__fill_mysql(result,count)
            return 'mysql'
        else:
            url=self.keyword_url.format(keyword,current_app.config['PER_PAGE'],self.calculate_start(page))
            result = HTTP.get(url)
            self.__fill_collection(result)
            return 'api'


    def calculate_start(self,page):
        return (page-1)*current_app.config['PER_PAGE']