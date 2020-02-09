from app.libs.helper import get_isbn


class BookViewModel:
    def __init__(self, data):
        # if not isinstance(data, dict):V
        #     author = data.author
        #     data = data.__dict__
        #     data['author'] = author
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.isbn = get_isbn(data)
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, rec_book, keyword,f='mysql'):
        self.total = rec_book.total
        if f=='api':
            self.books = [BookViewModel(book) for book in rec_book.books]
        else:
            self.books=[BookViewModelSQL(book) for book in rec_book.books]
        self.keyword = keyword

class BookViewModelSQL:
    def __init__(self, data):
        # if not isinstance(data, dict):V
        #     author = data.author
        #     data = data.__dict__
        #     data['author'] = author
        self.title = data.title
        self.author = data.author
        self.binding = data.binding
        self.publisher = data.publisher
        self.image = data.image
        self.price = data.price if data.price else data.price
        #self.isbn = get_isbn(data)
        self.isbn=data.isbn
        self.pubdate = data.pubdate
        self.summary = data.summary
        self.pages = data.pages

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)