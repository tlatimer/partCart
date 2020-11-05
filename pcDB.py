import sqlite3

class pcDB:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def search(self, table, col, val):
        vallike = '%{}%'.format(val)
        self.c.execute('select ? from ? where ? like ?',
                       (col, table, col, vallike)
                       )

        return self.c.fetchall()