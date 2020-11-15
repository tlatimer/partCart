import pcDB
from tabulate import tabulate
import settings as s
import termcolor


def main():
    p = pcCLI()
    p.mainMenu()
    # p.showParts([1,2])

    # a = p.findParts()
    # print('id: {}'.format(a))


class pcCLI():
    def __init__(self):
        self.db = pcDB.pcDB()

    def mainMenu(self):
        while True:
            print("""
======= MAIN MENU =======       
    1. [F]ind parts
    2. [M]ass change quantity
    3. [C]hange parts
    4. [I]nventory""")
            choice = input('?')

            choice = choice[:1].lower()
            if choice == '':
                # didn't press anything...?
                continue
            elif choice in ['1', 'f']:
                myPart = self.findParts()
                if myPart == None:
                    continue
                self.showPart(myPart)
            elif choice in ['2', 'm']:
                print('not implemented yet')
                continue
            elif choice in ['3', 'c']:
                print('not implemented yet')
                continue
            elif choice in ['4', 'i']:
                print('not implemented yet')
                continue

    def partMenu(self, id):
        print("""
======= PART MENU =======
    1. See [L]inked parts
    2. [S]ell quantity
    3. Link part to [G]roup
    4. [B]ack to Main Menu""")
        choice = input('?')

        choice = choice[:1].lower()
        while True:
            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'l']:
                print('not implemented yet')
                continue
            elif choice in ['2', 's']:
                print('not implemented yet')
                continue
            elif choice in ['3', 'g']:
                print('not implemented yet')
                continue

    def findParts(self):
        toSearch = input('Search for?')

        if not toSearch:
            return None

        ids = self.db.searchParts(toSearch)

        choices = self.showParts(ids, toSearch)
        choice = input('Which Part [#]?')

        try:
            if not choice:
                return None
            else:
                return choices[int(choice)]
        except:
            print('Invalid Choice!')
            return None

    def showPart(self, id):
        part = self.db.getPart(id)


        print('\n')
        for col in s.partCols:
            if part[col]:
                print('{:>11}: {}'.format(s.displayNames[col], part[col]))
            else:
                print('{:>11}:'.format(s.displayNames[col]))

        self.partMenu(id)


    def showParts(self, ids, searchTerm):
        parts = []
        for id in ids:
            parts.append(self.db.getPart(id))

        toReturn = {}
        table=[]
        for i, part in enumerate(parts):
            i += 1
            toReturn[i] = part['id']
            partRow = ['{}:'.format(i)]
            for col in s.searchCols:
                toAdd = str(part[col]).replace(searchTerm, termcolor.colored(searchTerm, 'yellow'))
                partRow.append(toAdd)
            table.append(partRow)

        print(tabulate(table, headers=s.showPartsHeader, tablefmt='github'))

        return toReturn


# main()
p = pcCLI()
p.mainMenu()