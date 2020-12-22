import pcDB2
from tabulate import tabulate
import settings as s

from termcolor import colored
import os
os.system('color')


def printYLW(text):
    print(colored(text, 'yellow'))


def prompt(text):
    return input('{:>20}?'.format(text)).strip().upper()


def printAligned(left, right):
    print('{:>14}:{}'.format(left, right))


class pcCLI:
    def __init__(self):
        self.db = pcDB2.pcDB(s.db_fname)

    def search(self):
        os.system('cls')
        term = prompt('Search for')
        if not term:
            return

        i = self.db.selectByExact(term, 'barcode')
        j = self.db.selectByExact(term, 'partnum')

        bins = [x['bin'] for x in i+j]

        if len(set(bins)) == 1:
            if i:  # is barcode
                printYLW('Found one part by BARCODE')
                return i[0]
            else:
                printYLW('Found one part by PART NUM')
                return j[0]

        allresults = self.db.selectByLike(term)

        if len(allresults) > 1:
            to_return = self.chooseResult(allresults, term)
            os.system('cls')
            return to_return
        elif len(allresults) == 1:
            printYLW('Found one part by SEARCH')
            return allresults[0]
        else:  # no results found
            printYLW('No results, would you like to add a new part?')
            if prompt('[y/N]') == 'Y':
                return self.newBin()
            else:
                return self.search()

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
                    partRow.append('-')
                    continue

                if col == '||':
                    partRow.append('||')
                    continue

                toAdd = str(part[col])
                if toAdd == 'NONE':
                    partRow.append('')
                    continue

                if col in s.colsToSearch and searchTerm:
                    toAdd = toAdd.replace(searchTerm, colored(searchTerm, 'cyan'))

                partRow.append(toAdd)

            table.append(partRow)
            prevbin = part['bin']

        # actually print out the table
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
                    return
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

        print(colored('CrossRefs for this part:', 'cyan'))
        headers = [s.displayNames[col] for col in cols]
        print(tabulate(table, headers=headers, tablefmt='pretty'))

        cols = ['desc', 'loc', 'sellprice', 'qty', 'lastsold']
        for c in cols:
            to_print = part[c]
            if not to_print:
                to_print = ''
            printAligned(s.displayNames[c], to_print)

    def massQtyChange(self, changeType):
        printYLW('Press [Enter] to return to main menu.')
        while True:
            os.system('cls')
            myPart = self.search()
            if myPart is None:
                return
            os.system('cls')
            self.showPart(myPart)
            self.changeQty(myPart, changeType)

    def changeQty(self, part, changeType):
        while True:
            qty = prompt(f'Qty to {changeType}')

            if qty == '':
                return
            try:
                qty = int(qty)
                break
            except:
                printYLW('Invalid Qty!')

        if changeType == 'sell':
            qty = -qty

        self.db.changeQty(part['bin'], qty)
        return self.db.selectByExact(part['bin'], 'bins.id')[0]

    def addCrossRef(self, part=None):
        if not part:
            part = self.search()
            if not part:
                return
            self.showPart(part)

        to_insert = {'bin': part['bin']}
        printYLW('Enter data for new CrossRef:')
        for i in s.all_crossref_cols:
            to_insert[i] = prompt(s.displayNames[i])

        self.db.doInsert('crossrefs', to_insert)

    def newBin(self):
        printYLW('Please enter data for the PART')
        bin_data = dict()
        for i in s.all_bin_cols:
            bin_data[i] = prompt(s.displayNames[i])

        bin_id = self.db.doInsert('bins', bin_data)

        printYLW('Now, Please enter data for the initial CrossRef')
        first_crossref = {'bin': bin_id}
        for i in s.all_crossref_cols:
            first_crossref[i] = prompt(s.displayNames[i])

        self.db.doInsert('crossrefs', first_crossref)

        while True:
            printYLW('Would you like to add another CrossRef?')
            if prompt('[y/N]') == 'Y':
                cur_part = self.db.selectByExact(bin_id, 'bins.id')[0]
                self.addCrossRef(cur_part)
            else:
                break

        printYLW('Now, Please enter the initial Qty')
        self.changeQty({'bin': bin_id}, 'start')

        return self.db.selectByExact(bin_id, 'bins.id')[0]


# p = pcCLI()
# while True:
#     i = prompt('Search for')
#     part = p.search(i)
#     p.showPart(part)
