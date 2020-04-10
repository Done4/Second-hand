from .book import BookViewModelSQL

class MyGifts:
    def __init__(self, gifts, wishes_count):
        #处理完放到gifts 里面 用作显示
        self.gifts = []
        self.__gifts_of_mine = gifts
        self.__wish_count__list = wishes_count
        self.gifts = self.__parse()


    def __parse(self):
        temp_gifts=[]
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self,gift):
         count = 0
         for wish_count in self.__wish_count__list:
             #找到对应的书，显示求赠着数量 默认为 0
            if gift.isbn == wish_count['isbn']:
                count = wish_count
         r = {
             'wishes_count': count,
             'book': BookViewModelSQL(gift.book),
             'id': gift.id
         }
         return r