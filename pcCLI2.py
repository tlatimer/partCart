import pcDB2
from tabulate import tabulate
import settings as s

from termcolor import colored
import os
os.system('color')

class pcCLI:
    def __init__(self):
        self.db = pcDB2.pcDB(s.dbfname)

    def mainMenu(self):
        while True:
            i = input()
            r = self.db.selectByExact(i)
            if r:
                print('exact match by {}'.format(r[0]))
                continue

            r = self.db.selectByLike(i)
            if r:
                print('fuzzy match by like')
                print(len(r[1]))
            else:
                print('no match found')

p = pcCLI()
p.mainMenu()