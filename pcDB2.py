import sqlite3
import settings as s

class pcDB:
    def __init__(self, filename):
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
        order by lastsold desc, bins.id desc
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