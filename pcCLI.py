import pcDB
from tabulate import tabulate
import settings as s

# from termcolor import colored
# stupid cmd doesn't understand colors.
def colored(str, color):
    return str

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
                self.partMenu(myPart)

            elif choice in ['2', 'm']:
                self.massQtyChange()
            elif choice in ['3', 'n']:
                self.updatePartFlow()
            elif choice in ['4', 'i']:
                print('inventory not implemented yet')  # TODO

    def partMenu(self, part):
        showPart = True
        while True:
            if showPart:
                self.showPart(part)
            else:
                showPart = True

            print(
                """======= PART MENU =======
    1. See [L]inked parts
    2. [S]ell quantity
    3. [E]dit part
    4. [B]ack to Main Menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'l']:
                parts = self.db.selectParts(crossref=part['crossref'])
                self.showSearch(parts)
                showPart = False
            elif choice in ['2', 's']:
                self.sellQty(part)
            elif choice in ['3', 'e']:
                r = self.editPartMenu(part)
                if r:  # something got returned
                    part = r

    def editPartMenu(self, part):

        while True:
            print(
                """======= EDIT MENU =======
    1. Link part to [C]rossref
    2. [E]dit part fields
    3. [D]elete part
    4. [B]ack to previous menu""")
            choice = input('?')

            choice = choice[:1].lower()
            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'c']:
                return self.linkPart(part)
            elif choice in ['2', 'e']:
                self.updatePartFlow(part)
                return
            elif choice in ['3', 'd']:
                print('delete not implemented yet')  # TODO

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
                    elif choice == '':
                        return None
                    else:
                        return choices[int(choice)]
                except:
                    print('Invalid choice! try again.')

        elif len(rows) == 1:
            message = colored("Only 1 part was found", 'yellow')
            print(message)
            return rows[0]
        else:
            i = input("No parts found. Would you like to add a part with barcode '%s' [y/N]?" % toSearch)
            if i.lower()[:1] == 'y':
                self.updatePartFlow({'barcode': toSearch})


    def showPart(self, part):
        print('\n======= PART DATA =======')
        for col in s.allPartCols:
            if part[col]:
                print('{:>14}: {}'.format(s.displayNames[col], part[col]))
            else:
                print('{:>14}:'.format(s.displayNames[col]))

    def showSearch(self, rows, searchTerm=None):
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
                if col in s.colsToSearch and searchTerm:
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
                    data[col] = newVal
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

    def linkPart(self, part):
        if part['crossref']:
            # part is already linked
            i = input('Would you like to remove this Crossref [y/N]?')
            if i.lower()[:1] == 'y':
                self.db.updatePart(part['id'], {'crossref': None})

        else:
            # part is not linked
            print(colored('What part would you like to link it to?', 'yellow'))
            part2 = self.findParts()
            if part2 is None:
                return

            if part2['crossref']:
                #part2 is linked, copy to part
                self.showPart(part2)
                i = input('Are you sure you\'d like to link to this part [y/N]?')
                if i.lower()[:1] == 'y':
                    self.db.updatePart(part['id'], {'crossref': part2['crossref']})
            else:
                # part2 is not linked; create new crossref
                pass

        return self.db.selectParts(id=part['id'])

p = pcCLI()
p.mainMenu()