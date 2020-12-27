import sqlite3
import settings as s


class pcDB:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def doInsert(self, table, data):
        if not ''.join([i for i in data.values() if type(i) == str]):
            print('No data entered! No changes made to database.')
            return
        cols = ', '.join(data.keys())
        qmarks = ', '.join(['?'] * len(data))
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, cols, qmarks)

        self.c.execute(query, list(data.values()))
        self.conn.commit()
        return self.c.lastrowid

    def doUpdate(self, table, dataDict, id):
        if 'id' in dataDict:
            del(dataDict['id'])

        setCols = []
        for k in dataDict.keys():
            setCols.append('{} = ?'.format(k))

        query = 'UPDATE {} SET ' + ', '.join(setCols) + ' WHERE id = ?'
        query = query.format(table)

        args = list(dataDict.values()) + [id]

        self.c.execute(query, args)
        self.conn.commit()

    def doSelect(self, where_clause, search_vals):
        query = """
        select 
        
        bins.*, 
        crossrefs.*, 
        sum(qtychange) as qty, 
        max(timestamp) as lastsold 
        
        from bins
        inner join crossrefs on bins.id = crossrefs.bin
        left outer join qtychanges on bins.id = qtychanges.bin
        
        where {}
        
        group by crossrefs.id
        order by lastsold desc, bins.id desc, crossrefs.id
        """
        query = query.format(where_clause)

        if not type(search_vals) is list:
            search_vals = (search_vals,)

        return self.c.execute(query, search_vals).fetchall()

    def selectByExact(self, search_for, column):
        where_clause = '{} = ?'.format(column)
        return self.doSelect(where_clause, search_for)

    def selectByLike(self, search_for):
        where_clause = ' OR '.join(['{} LIKE ?'.format(i) for i in s.colsToSearch])
        search_vals = ['%{}%'.format(search_for)] * len(s.colsToSearch)
        return self.doSelect(where_clause, search_vals)

    def changeQty(self, id, change):
        argDict = {
            'bin': id,
            'qtychange': change,
            # 'timestamp': "datetime('now')"  # TODO gonna have to do this in raw SQL
            'timestamp': "-"
        }
        self.doInsert('qtyChanges', argDict)

    def deleteBin(self, bin_id):
        query = "delete from crossrefs where bin = ?"
        self.c.execute(query, (bin_id,))

        query = "delete from bins where id = ?"
        self.c.execute(query, (bin_id,))
        self.conn.commit()

    def deleteCrossRef(self, bin_id):  # TODO low
        pass

    def updateOrInsert(self, table, data):
        if 'id' in data:
            self.doUpdate(table, data, data['id'])
        else:
            self.doInsert(table, data)
