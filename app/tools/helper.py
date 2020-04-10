def is_isbn_or_key(word):
    '''
    判断q是ISBN还是关键字
    isbn13 13个0-9数字组成
    isbn10 10个0-9数字组成 含有‘-’
    :param q:
    :return :
    '''
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    if '-' in word and len(word.replace('-', '')) == 10:
        # isbn10
        return 'isbn'
    return 'keyword'

#读取ISBN 有两种分别处理
def get_isbn(data_dict):
    isbn = data_dict.get('isbn')
    if not isbn:
        isbn = data_dict.get('isbn13')
        if not isbn:
            isbn = data_dict.get('isbn10')
    return isbn

