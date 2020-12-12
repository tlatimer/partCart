import pcCLI2

from termcolor import colored
import os
os.system('color')

class pcMenu2:
    def __init__(self):
        self.cli = pcCLI2.pcCLI()

    def mainMenu(self):
        while True:
            print("""
======= MAIN MENU =======       
    1. [F]ind parts
    2. [M]ass enter sales
    3. [N]ew Part
    4. [I]nventory""")
            choice = input('?')

            choice = choice[:1].lower()
            if choice in ['1', 'f']:
                myPart = self.cli.search()
                if myPart is None:
                    continue
                self.partMenu(myPart)

            elif choice in ['2', 'm']:
                self.cli.massQtyChange('sell')
            elif choice in ['3', 'n']:
                self.updatePartFlow()
            elif choice in ['4', 'i']:
                self.invMenu()

    def partMenu(self, part):
        self.cli.showPart(part)
        while True:
            print(
                """======= PART MENU =======
    2. [S]ell quantity
    3. [E]dit part
    4. [B]ack to Main Menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['2', 's']:
                part = self.sellQty(part, type='sell')
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
                i = input('Type this exactly: [{}]?'.format(colored('Please Delete Me', 'red')))
                if i == 'Please Delete Me':
                    self.db.deletePart(part['id'])
                    return
                else:
                    print("It didn't match exactly. Capitals are important, too.")

    def invMenu(self):
        while True:
            print(
                """======= INVENTORY MENU =======
    1. [R]eceive new parts
    2. [A]udit inventory
    4. [B]ack to previous menu""")
            choice = input('?')

            choice = choice[:1].lower()
            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'r']:
                self.massQtyChange('receive')
            elif choice in ['2', 'a']:
                self.doAudit()
            elif choice in ['3', 'h']:
                print('history not implemented yet')  # TODO

p = pcMenu2()
p.mainMenu()