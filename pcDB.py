import sqlite3
import settings as s


class pcDB:
    def __init__(self, filename='partCart.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def selectParts(self, id=None, search=None):
        query = """
            SELECT
    
            parts.*, 
            crossref.name,
            sum(qtyChange) as qty, 
            max(timestamp) as timestamp
            
            FROM parts 
            LEFT OUTER JOIN qtyChanges 
            ON parts.id = qtyChanges.part
            LEFT OUTER JOIN crossref
            on parts.crossref = crossref.id
            WHERE {}
            GROUP BY parts.id
            ORDER BY timestamp DESC"""

        if id:
            whereClause = "parts.id = ?"
            q = query.format(whereClause)

            return self.c.execute(q, (id,)).fetchone()
        elif search:
            whereClause = 'barcode = ?'
            q = query.format(whereClause)

            result = self.c.execute(q, (search,)).fetchall()
            if len(result) > 0:
                return result

            # didn't find it by barcode, now search for text
            whereClause = ' OR '.join(['%s LIKE ?' % i for i in s.colsToSearch])
            searchVals = ['%{}%'.format(search)] * len(s.colsToSearch)

            q = query.format(whereClause)
            return self.c.execute(q, searchVals).fetchall()

    # def searchParts(self, val):
    #     # asdf: return 1 where barcode = ?
    #     query = """
    #         SELECT id FROM parts WHERE
    #         OR desc LIKE ?
    #         OR partnum LIKE ?
    #         OR notes LIKE ?
    #     """
    #     # asdf: order by qtychanges.timestamp desc
    #     vallike = '%{}%'.format(val)
    #     result = self.c.execute(query, [vallike]*3).fetchall()
    #
    #     ids = [i[0] for i in result]
    #
    #     return ids
    #
    # def getPart(self, id):
    #     query = """
    #         SELECT parts.*, sum(qtyChange) as qty, max(timestamp) as timestamp
    #         FROM parts
    #         LEFT OUTER JOIN qtyChanges
    #         ON parts.id = qtyChanges.part
    #         WHERE parts.id = ?
    #     """
    #     id = int(id)
    #     return self.c.execute(query, (id,)).fetchone()

    def insertPart(self, partDict):
        cols = ', '.join(partDict.keys())
        qmarks = ', '.join(['?'] * len(partDict))
        query = 'INSERT INTO parts ({}) VALUES ({})'.format(cols, qmarks)

        self.c.execute(query, list(partDict.values()))
        self.conn.commit()

    def updatePart(self, id, partDict):
        if 'id' in partDict:
            del(partDict['id'])

        setCols = []
        for k in partDict.keys():
            setCols.append('{} = ?'.format(k))

        query = 'UPDATE parts SET ' + ', '.join(setCols) + ' WHERE id = ?'
        args = list(partDict.values())+[id]

        self.c.execute(query, args)
        self.conn.commit()

    def deletePart(self, id):
        pass  # TODO

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

    def newCrossef(self, name):
        query = 'INSERT INTO crossref (name) VALUES (?)'
        self.c.execute(query, (name,))
        self.conn.commit()
        return self.c.lastrowid

    def linkParts(self, id1, id2):
        pass  # TODO

    def getLinkedParts(self, id):
        pass  # TODO


# a = pcDB()
# print(a.getQty(3))