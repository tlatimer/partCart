import sqlite3

class pcDB:
    def __init__(self, filename='partCart.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()


    def search(self, table, col, val):
        vallike = '%{}%'.format(val)
        self.c.execute('select ? from ? where ? like ?',
                       (col, table, col, vallike)
                       )

        return self.c.fetchall()

    def addPart(self, partDict):
        cols = ', '.join(partDict.keys())
        qmarks = ', '.join(['?'] * len(partDict))
        query = 'INSERT INTO parts ({}) VALUES ({})'.format(cols, qmarks)

        self.c.execute(query, list(partDict.values()))
        self.conn.commit()


    def updatePart(self, id, partDict):
        setCols = []
        for k in partDict.keys():
            setCols.append('{} = ?'.format(k))

        query = 'UPDATE parts SET ' + ', '.join(setCols) + ' WHERE id = ?'
        args = list(partDict.values())+[id]

        self.c.execute(query, args)
        self.conn.commit()

    def changeQty(self, id, change, user=1, notes=''):
        argDict = {
            'user': user,
            'timestamp': 'datetime(now)',
            'part': id,
            'qtychange': change,
            'notes': notes,
        }
        cols = ', '.join(argDict.keys())
        qmarks = ', '.join(['?'] * len(partDict))
        query = 'INSERT INTO qtyChanges ({}) VALUES ({})'.format(cols, qmarks)

        self.c.execute(query, list(argDict.values()))
        self.conn.commit()

    def getQty(self, id):
        query = 'SELECT sum(qty) FROM qtyChanges WHERE part = ?'

        result = self.c.execute(query, (id,)).fetchone()
        return result[0]

    def linkParts(self, id1, id2):
        pass


    def getLinkedParts(self, part):
        pass