import sqlite3
import settings as s

class pcDB:
    def __init__(self, filename=s.dbfname):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def doInsert(self, table, data):
        cols = ', '.join(data.keys())
        qmarks = ', '.join(['?'] * len(data))
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, cols, qmarks)

        self.c.execute(query, list(data.values()))
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
        order by bins.id
        """
        query = query.format(where_clause)

        if not type(search_vals) is list:
            search_vals = (search_vals,)

        return self.c.execute(query, search_vals).fetchall()

    def selectByExact(self, search_for):
        r = self.doSelect('barcode = ?', search_for)
        if len(r) > 0:
            return['barcode', r]

        r = self.doSelect('partnum = ?', search_for)
        if len(r) > 0:
            return['partnum', r]

        return None

    def selectByLike(self, search_for):
        where_clause = ' OR '.join(['%s LIKE ?' % i for i in s.colsToSearch])
        search_vals = ['%{}%'.format(search_for)] * len(s.colsToSearch)

        r = self.doSelect(where_clause, search_vals)
        if len(r) > 0:
            return['like', r]
        else:
            return None
