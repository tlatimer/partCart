import sqlite3
import settings as s

class gf:
    def __init__(self, filename='partCart.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()