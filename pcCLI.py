import pcDB
from tabulate import tabulate
import settings as s
from termcolor import colored


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
    3. [N]ew Part
    4. [I]nventory""")
            choice = input('?')

            choice = choice[:1].lower()
            if choice in ['1', 'f']:
                myPart = self.findParts()
                if myPart is None:
                    continue
                self.showPart(myPart)

            elif choice in ['2', 'm']:
                self.massQtyChange()
            elif choice in ['3', 'n']:
                self.updatePartFlow()
            elif choice in ['4', 'i']:
                print('not implemented yet')  # TODO

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
                print('not implemented yet')  # TODO
            elif choice in ['2', 's']:
                self.sellQty(part)
            elif choice in ['3', 'e']:
                self.editPartMenu(part)

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
                print('not implemented yet')  # TODO
            elif choice in ['2', 'e']:
                self.updatePartFlow(part)
                return
            elif choice in ['3', 'd']:
                print('not implemented yet')  # TODO

    def findParts(self):
        toSearch = input('{:>14}?'.format('Search for'))

        if not toSearch:
            return None

        rows = self.db.selectParts(search=toSearch)

        if len(rows) > 1:
            choices = self.showSearch(rows, toSearch)
            while True:
                choice = input('{:>14}?'.format('Which Part [#]'))
                try:
                    if choice.lower() == 'f':
                        return self.findParts()
                    elif choice.lower() == '':
                        return None
                    else:
                        return choices[int(choice)]
                except:
                    print('Invalid choice! try again')

        elif len(rows) == 1:
            message = colored("Only 1 part was found", 'yellow')
            print(message)
            return rows[0]
        else:
            pass  #TODO: 'no parts found, would you like to add a part with the barcode x'

    def showPart(self, part):
        print('\n======= PART DATA =======')
        for col in s.allPartCols:
            if part[col]:
                print('{:>14}: {}'.format(s.displayNames[col], part[col]))
            else:
                print('{:>14}:'.format(s.displayNames[col]))

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
                if col in s.colsToSearch:
                    toAdd = toAdd.replace(searchTerm, colored(searchTerm, 'yellow'))
                partRow.append(toAdd)
            table.append(partRow)

        print(tabulate(table, headers=s.findPartsHeader, tablefmt='github'))

        return toReturn

    def updatePartFlow(self, prevData=None):
        if prevData is None:
            data = dict()
        else:
            data = dict(prevData)

        for k in [*data.keys()]:
            if data[k] in [None, '']:
                del(data[k])

        print(colored('Press [Enter] to leave unchanged or blank.', 'yellow'))
        for col in s.updateCols:
            if col in data:
                print('{:>14}: {}'.format(s.displayNames[col], prevData[col]))
                newVal = input(' '*14 + '?')
                if newVal != '':
                    data[col] = i
            else:
                data[col] = input('{:>14}?'.format(s.displayNames[col]))


        if 'id' in data:
            # action = 'update'
            self.db.updatePart(id=data['id'], partDict=data)
        else:
            # action = 'insert'
            self.db.insertPart(partDict=data)

    def sellQty(self, part, notes=None):
        while True:
            qty = input('{:>14}?'.format('Qty'))

            if qty == '':
                return

            try:
                qty = int(qty)
                if notes is None:
                    notes = input('{:>14}?'.format('Notes'))
                self.db.changeQty(part['id'], -qty, notes)

                return

            except:
                "Invalid quantity"

    def massQtyChange(self):
        print(colored('Press [Enter] to return to main menu.', 'yellow'))
        while True:
            myPart = self.findParts()
            if myPart is None:
                return
            self.sellQty(myPart, 'mass')


# main()
p = pcCLI()
p.mainMenu()