import sqlite3
import random

randvendors = ['asdf', 'qwer', 'zxcv', 'wasd']

randletters= ' qwerasdfzxcvtgb '.upper()

nums = [500, 5000, 5000]



class gf:
    def __init__(self, filename='partCart2.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

        for i in ['bins', 'crossrefs', 'qtychanges']:
            self.c.execute('delete from {}'.format(i))
        self.conn.commit()

    def getRandLetters(self, a, b):
        return ''.join(random.choices(randletters, k=random.randint(a, b)))

    def doInsert(self, table, data):
        cols = ', '.join(data.keys())
        qmarks = ', '.join(['?'] * len(data))
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, cols, qmarks)

        for k in data.keys():
            if type(data[k]) is str:
                data[k] = data[k].strip()

        self.c.execute(query, list(data.values()))

    def doRandShit(self):
        for i in range(nums[0]):
            dict = {
                'desc': self.getRandLetters(15, 20),
                'loc': self.getRandLetters(7, 11),
            }
            self.doInsert('bins', dict)

        self.conn.commit()

        bin_ids = self.c.execute('select id from bins').fetchall()
        bin_ids = [i[0] for i in bin_ids]
        for i in range(nums[1]):
            dict = {
                'bin': random.choice(bin_ids),
                'vendor': random.choice(randvendors),
                'partnum': self.getRandLetters(7, 11),
                'barcode': i*1000,
            }

            if random.random() > 0.8:
                dict['barcode'] = dict['partnum']

            self.doInsert('crossrefs', dict)

        almost_all_bins = nums[0] - int(nums[0]/8)
        almost_all_bins = bin_ids[:almost_all_bins]
        for i in range(nums[2]):
            dict = {
                'bin': random.choice(almost_all_bins),
                'qtychange': random.randint(-50, 50),
                'timestamp': i*1000,
            }
            self.doInsert('qtychanges', dict)

        self.conn.commit()


db = gf()
db.doRandShit()
