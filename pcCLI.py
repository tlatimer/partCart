import pcDB
from tabulate import tabulate

fields = [
            'name',
            'mfr',
            'model',
            'qty',
            'cost',
            'price',
            'notes',
        ]

def main():
    p = pcCLI()
    # p.showParts([1,2])

    # a = p.findParts()
    # print('id: {}'.format(a))

    p.mainMenu()


class pcCLI():
    def __init__(self):
        self.db = pcDB.pcDB()

    def mainMenu(self):
        while True:
            print("""
    1. [F]ind parts
    2. [M]ass change quantity
    3. [N]ew part
            """)
            choice = input('?')

            if choice == '':
                continue

            choice = choice[0].lower()
            if choice in ['1', 'f']:
                myPart = self.findParts()
                if myPart == None:
                    continue
                self.showPart(myPart)
            elif choice in ['2', 'm']:
                # TODO
                print('not implemented yet')
                continue
            elif choice in ['3', 'n']:
                # TODO
                print('not implemented yet')
                continue



    def findParts(self):
        toSearch = input('Search Term?')

        if not toSearch:
            return None

        ids = self.db.searchParts(toSearch)

        choices = self.showParts(ids)
        choice = input('Which Part [#] (or blank to cancel)?')

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
        for f in fields:
            if part[f]:
                print('{:>5}: {}'.format(f, part[f]))
            else:
                print('{:>5}:'.format(f))

        self.partMenu(id)

    def partMenu(self, id):
        print("""
    1. Adjust [q]uantity
    2. [E]dit part
    3. See [L]inked parts
    4. Link part to [g]roup
    5. [B]ack
                    """)
        choice = input('?')

        choice = choice[0].lower()
        while True:
            if choice in ['', '5', 'b']:
                return
            elif choice in ['1', 'q']:
                # TODO
                print('not implemented yet')
                continue
            elif choice in ['2', 'e']:
                # TODO
                print('not implemented yet')
                continue
            elif choice in ['3', 'l']:
                # TODO
                print('not implemented yet')
                continue
            elif choice in ['4', 'g']:
                # TODO
                print('not implemented yet')
                continue

    def showParts(self, ids):
        parts = []
        for id in ids:
            parts.append(self.db.getPart(id))

        header = fields[:-1]

        toReturn = {}
        table=[]
        for i, part in enumerate(parts):
            i += 1
            toReturn[i] = part['id']
            partRow = ['{}: '.format(i)]
            for h in header:
                partRow.append(part[h])
            table.append(partRow)

        header = ['[#]'] + header

        print(tabulate(table, headers=header, tablefmt='github'))

        return toReturn


main()