import sqlite3

class pcDB:
    def __init__(self, filename='partCart.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()


    def searchParts(self, val):
        query = """
            SELECT id FROM parts WHERE
            OR desc LIKE ?
            OR partnum LIKE ?
            OR notes LIKE ?
        """
        vallike = '%{}%'.format(val)
        result = self.c.execute(query, (
            val,
            vallike,
            vallike,
            vallike,
        )).fetchall()

        result = [i[0] for i in result]

        return result


    def getPart(self, id):
        query = """
            SELECT parts.*, sum(qtyChange) as qty
            FROM parts 
            LEFT OUTER JOIN qtyChanges 
            ON parts.id = qtyChanges.part
            WHERE parts.id = ?
        """
        id = int(id)
        return self.c.execute(query, (id,)).fetchone()


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

    def changeQty(self, id, change, notes=''):
        argDict = {
            'part': id,
            'qtychange': change,
            'notes': notes,
        }
        cols = ', '.join(argDict.keys())
        qmarks = ', '.join(['?'] * len(argDict))
        query = "INSERT INTO qtyChanges (timestamp, {}) VALUES (datetime('now'), {})".format(cols, qmarks)

        self.c.execute(query, list(argDict.values()))
        self.conn.commit()


    def linkParts(self, id1, id2):
        pass


    def getLinkedParts(self, id):
        pass


# a = pcDB()
# print(a.getQty(3))