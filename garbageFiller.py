import sqlite3
import random

randvendors = ['asdf', 'qwer', 'zxcv', 'wasd']

randletters= ' qwerasdfzxcvtgb '


class gf:
    def __init__(self, filename='partCart2.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def getRandLetters(self, a, b):
        return ''.join(random.choices(randletters, k=random.randint(a, b)))

    def doInsert(self, table, data):
        cols = ', '.join(data.keys())
        qmarks = ', '.join(['?'] * len(data))
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, cols, qmarks)

        self.c.execute(query, list(data.values()))
        self.conn.commit()

    def doRandShit(self):
        for i in range(20):
            dict = {
                'desc': self.getRandLetters(15, 20),
                'loc': self.getRandLetters(7, 11),
                'sellprice': 0,
            }
            self.doInsert('bins', dict)


        bin_ids = self.c.execute('select id from bins').fetchall()
        bin_ids = [i[0] for i in bin_ids]
        for i in range(50):
            dict = {
                'bin': random.choice(bin_ids),
                'vendor': random.choice(randvendors),
                'partnum': self.getRandLetters(7, 11),
                'barcode': i*1000,
                'cost': 0,
            }
            self.doInsert('crossrefs', dict)

        for i in range(200):
            dict = {
                'bin': random.choice(bin_ids[:-3]),
                'qtychange': random.randint(-50, 50),
                'timestamp': i*1000,
            }
            self.doInsert('qtychanges', dict)


db = pcDB()
db.doRandShit()
