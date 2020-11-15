import pcDB
from tabulate import tabulate
import settings as s
import termcolor


def main():
    # TODO: bring main() up from bottom of file
    pass


class pcCLI:
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
            if choice in ['1', 'f']:
                myPart = self.findParts()
                if myPart is None:
                    continue
                self.showPart(myPart)
            elif choice in ['2', 'm']:
                print('not implemented yet')
            elif choice in ['3', 'c']:
                print('not implemented yet')
            elif choice in ['4', 'i']:
                print('not implemented yet')

    def partMenu(self, part):
        print(
"""======= PART MENU =======
    1. See [L]inked parts
    2. [S]ell quantity
    3. [E]dit part
    4. [B]ack to Main Menu""")
        choice = input('?')

        choice = choice[:1].lower()
        while True:
            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'l']:
                print('not implemented yet')
            elif choice in ['2', 's']:
                print('not implemented yet')
            elif choice in ['3', 'g']:
                print('not implemented yet')

    def editPartMenu(self, part):
        print(
"""======= EDIT MENU =======
    1. Link part to [G]roup
    2. [E]dit part fields
    3. [D]elete part
    4. [B]ack to previous menu""")
        choice = input('?')

        choice = choice[:1].lower()
        while True:
            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'g']:
                print('not implemented yet')
            elif choice in ['2', 'e']:
                print('not implemented yet')
            elif choice in ['3', 'd']:
                print('not implemented yet')

    def findParts(self):
        toSearch = input('Search for?')

        if not toSearch:
            return None

        rows = self.db.selectParts(search=toSearch)

        if len(rows) > 1:
            choices = self.showSearch(rows, toSearch)
            while True:
                choice = input('Which Part [#]?')
                try:
                    return choices[int(choice)]
                except:
                    print('Invalid choice! try again')

        elif len(rows) == 1:
            message = termcolor.colored("Only 1 part was found", 'yellow')
            print(message)
            return rows[0]
        else:
            pass  #TODO: 'no parts found, would you like to add a part with the barcode x'

    def showPart(self, part):
        print('\n======= PART DATA =======')
        for col in s.partCols:
            if part[col]:
                print('{:>11}: {}'.format(s.displayNames[col], part[col]))
            else:
                print('{:>11}:'.format(s.displayNames[col]))

        self.partMenu(part)

    def showSearch(self, rows, searchTerm):
        toReturn = {}
        table=[]
        for i, part in enumerate(rows):
            i += 1
            toReturn[i] = part
            partRow = ['{}:'.format(i)]
            for col in s.searchCols:
                toAdd = str(part[col])
                if toAdd == 'None':
                    partRow.append('')
                    continue
                if col != 'vendor':
                    toAdd = toAdd.replace(searchTerm, termcolor.colored(searchTerm, 'yellow'))
                partRow.append(toAdd)
            table.append(partRow)

        print(tabulate(table, headers=s.findPartsHeader, tablefmt='github'))

        return toReturn


# main()
p = pcCLI()
p.mainMenu()