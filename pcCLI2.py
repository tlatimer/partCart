import pcDB2
from tabulate import tabulate
import settings as s

from termcolor import colored
import os
os.system('color')


def printYLW(text):
    print(colored(text, 'yellow'))


def prompt(text):
    return input('{:>14}?'.format(text)).strip().upper()


class pcCLI:
    def __init__(self):
        self.db = pcDB2.pcDB(s.dbfname)

    def search(self, term):
        i = self.db.selectByExact(term, 'barcode')
        j = self.db.selectByExact(term, 'partnum')

        if len(i+j) == 1 or len(i+j) == 2 and i == j:
            if i:  # is barcode
                printYLW('Found one part by BARCODE')
                return i[0]
            else:
                printYLW('Found one part by PART NUM')
                return j[0]

        allresults = i + j + self.db.selectByLike(term)

        if len(allresults) > 1:
            return self.chooseResult(allresults, term)
        elif len(allresults) == 1:
            printYLW('Found one part by SEARCH')
            return allresults[0]
        else:  # no results found
            printYLW('No parts found, would you like to add a part with this barcode [y/N]?')
            i = input('?')
            if i[:-1].lower() == 'y':
                self.updatePart({'barcode': term})
                return  # TODO not sure what to return here, if anything

    def chooseResult(self, allresults, searchTerm):
        choices = {}
        table = []
        prevbin = allresults[0]['bin']

        for i, part in enumerate(allresults):
            if part['bin'] != prevbin:
                table.append([''] * len(s.searchDisplayCols))


            i += 1
            choices[i] = part

            partRow = ['{}:'.format(i)]
            for col in s.searchDisplayCols:
                if part['bin'] == prevbin and col in s.binDispCols and i != 1:
                    partRow.append('"')
                    continue

                if col == '||':
                    partRow.append('||')
                    continue

                toAdd = str(part[col]).upper()
                if toAdd == 'NONE':
                    partRow.append('')
                    continue

                if col in s.colsToSearch and searchTerm:
                    toAdd = toAdd.replace(searchTerm, colored(searchTerm, 'magenta'))

                partRow.append(toAdd)

            table.append(partRow)
            prevbin = part['bin']

        print(tabulate(table, headers=s.findPartsHeader, tablefmt='pretty'))

        while True:
            choice = prompt('Which Part [#]')
            try:
                if choice in ['', 'F']:
                    return None
                else:
                    return choices[int(choice)]
            except:
                print('Invalid choice! try again.')




    def updatePart(self, prevdata=dict()):  # TODO gonna be hard because of two tables
        pass


p = pcCLI()
while True:
    i = prompt('Search for')
    p.search(i)