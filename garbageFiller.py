import sqlite3
import random

randvendors = ['asdf', 'qwer', 'zxcv', 'wasd']

randletters= ' qwerasdfzxcvtgb '


class pcDB:
    def __init__(self, filename='partCart2.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def getRandLetters(self, a, b):
        return ''.join(random.choices(randletters, k=random.randint(a, b)))

    def doRandShit(self):
        for i in range(20):
            dict = {
                'desc': self.getRandLetters(15, 20),
                'loc': self.getRandLetters(7, 11),
                'sellprice': 0,
            }

            cols = ', '.join(dict.keys())
            qmarks = ', '.join(['?'] * len(dict))
            query = 'INSERT INTO bins ({}) VALUES ({})'.format(cols, qmarks)

            self.c.execute(query, list(dict.values()))
            self.conn.commit()

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

            cols = ', '.join(dict.keys())
            qmarks = ', '.join(['?'] * len(dict))
            query = 'INSERT INTO crossrefs ({}) VALUES ({})'.format(cols, qmarks)

            self.c.execute(query, list(dict.values()))
            self.conn.commit()

        for i in range(200):
            dict = {
                'bin': random.choice(bin_ids[:-3]),
                'qtychange': random.randint(-50, 50),
                'timestamp': i*1000,
            }

            cols = ', '.join(dict.keys())
            qmarks = ', '.join(['?'] * len(dict))
            query = 'INSERT INTO qtychanges ({}) VALUES ({})'.format(cols, qmarks)

            self.c.execute(query, list(dict.values()))
            self.conn.commit()


db = pcDB()
db.doRandShit()