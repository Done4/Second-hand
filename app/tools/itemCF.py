import math

from app.models.base import db


class ItemBasedCF:
    def __init__(self):
        self.readData()
        self.itemSimilarity()
    def readData(self):
        '''
        读取wish表 取出 uid isbn 计算出现次数作为喜好权重 记作score
        1.在定制sql处理
        2.用k in d.keys() 判断key在不在字典进行累加次数操作
        采用1方案，生成数据集train {uid:{ isbn:score }, { isbn:score } }
        {1: {'9787111127482': 1, '9787540213206': 2}, 2: {'9787020008728': 1}}
        '''
        self.train = {}
        sql = 'select uid,isbn,count(isbn) as score from wish group by uid,isbn'
        wish = db.session.execute(sql)
        results = wish.fetchall()
        for result in results:
            self.train.setdefault(result[0], {})
            self.train[result[0]][result[1]] = result[2]
    '''
    共现矩阵 {isbn : {isbn : count} }
    C {'9787111127482': {'9787540213206': 1}, '9787540213206': {'9787111127482': 1}, '9787020008728': {}}
    喜欢item的用户数 矩阵 {isbn : count}
    N {'9787111127482': 1, '9787540213206': 1, '9787020008728': 1}
    物品相似度计算公式： Wij=|N(i) and N(j)| / |sqrt(N(i)*N(j))|
    物品相似度矩阵 {isbn : { isbn : w} }
    W {'9787111127482':{'9787540213206': 1.0}}
    '''
    def itemSimilarity(self):
        self.W = {}
        C = {} #item - item 的共现矩阵
        N = {} #item被多少个不同用户购买
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1 #item-i 出现次数
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j: continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1 #item-i item-j 共现次数
        #计算相似度矩阵
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j,cij in related_items.items():
                #cij 为同时喜欢物品i和物品j的用户数 即上述计算的共现次数
                #N[i]为喜欢物品i的用户数 ，N[j]为喜欢物品i的用户数
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))

    #给user 推荐前N 的可能感兴趣的物品
    def recommend(self, user, N=6):
        rank = {}
        action_item = self.train[user]
        for item, score in action_item.items():
            for j, wj in self.W[item].items():
                #只推荐没买过的
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[:N]#排序后返回前n个物品

