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

def printAligned(left, right):
    print('{:>14}:{}'.format(left, right))


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
                    toAdd = toAdd.replace(searchTerm, colored(searchTerm, 'cyan'))

                partRow.append(toAdd)

            table.append(partRow)
            prevbin = part['bin']

        os.system('cls')
        toPrint = tabulate(table, headers=s.findPartsHeader, tablefmt='pretty')
        print(toPrint)

        if len(table) > 20:
            toPrint = toPrint.splitlines()
            for i in [1,2]:
                print(toPrint[i])

        while True:
            choice = prompt('Which Part [#]')
            try:
                if choice in ['', 'F']:
                    return None
                else:
                    return choices[int(choice)]
            except:
                print('Invalid choice! try again.')

    def showPart(self, part):
        data = self.db.selectByExact(part['bin'], 'bins.id')

        cols = ['vendor', 'partnum', 'barcode', 'cost']
        table = []
        for row in data:
            table.append([row[col] for col in cols])

        os.system('cls')
        print('CrossRefs for this part:')
        headers = [s.displayNames[col] for col in cols]
        print(tabulate(table, headers=headers, tablefmt='pretty'))

        cols = ['desc', 'loc', 'sellprice', 'qty', 'lastsold']
        for c in cols:
            printAligned(s.displayNames[c], part[c])

    def updatePart(self, prevdata=dict()):  # TODO gonna be hard because of two tables
        pass


p = pcCLI()
while True:
    i = prompt('Search for')
    part = p.search(i)
    p.showPart(part)
