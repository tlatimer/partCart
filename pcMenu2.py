import pcCLI2

from termcolor import colored
import os
os.system('color')

class pcMenu2:
    def __init__(self):
        self.cli = pcCLI2.pcCLI()

    def mainMenu(self):
        while True:
            os.system('cls')
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
                self.newMenu()
            elif choice in ['4', 'i']:
                self.invMenu()

    def partMenu(self, part):
        while True:
            self.cli.showPart(part)
            print(
                """
======= PART MENU =======
    2. [S]ell quantity
    3. [E]dit part
    4. [B]ack to Main Menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['2', 's']:
                part = self.cli.changeQty(part, changeType='sell')
            elif choice in ['3', 'e']:
                r = self.editPartMenu(part)
                if r:  # something got returned
                    part = r

    def editPartMenu(self, part):
        while True:
            print(
                """
======= EDIT MENU =======
    1. Add [C]rossref
    2. [E]dit part fields
    3. [D]elete part bin
    4. [B]ack to previous menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'c']:
                return self.cli.addCrossRef(part)
            elif choice in ['2', 'e']:
                pcCLI2.printYLW('Editing part fields isnt supported yet')  # TODO
                # self.updatePartFlow(part)
            elif choice in ['3', 'd']:
                i = input('Type this exactly: [{}]?'.format(colored('Please Delete Me', 'red')))
                if i == 'Please Delete Me':
                    self.db.deletePart(part['id'])  # TODO
                    return
                else:
                    print("It didn't match exactly. Capitals are important, too.")

    def invMenu(self):
        while True:
            os.system('cls')
            print(
                """
======= INVENTORY MENU =======
    1. [R]eceive new part shipment
    2. [A]udit inventory
    4. [B]ack to previous menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'r']:
                self.cli.massQtyChange('receive')
            elif choice in ['2', 'a']:
                pcCLI2.printYLW('Auditing isnt supported yet')  # TODO
                # self.doAudit()
            elif choice in ['3', 'h']:
                print('history not implemented yet')  # TODO

    def newMenu(self):
        while True:
            print(
                """
======= NEW PART MENU =======
    1. Add [C]rossRef to existing part bin
    2. [N]ew part bin
    4. [B]ack to previous menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'c']:
                self.cli.addCrossRef()
            elif choice in ['2', 'n']:
                self.cli.newBin()


while True:
    try:
        p = pcMenu2()
        p.mainMenu()
    except:
        raise
        pcCLI2.printYLW('ERROR: PROGRAM CRASHED. WRITE DOWN WHAT YOU JUST DID TO TELL TOM. 715-6827\n'
                        '  PRESS ENTER TO RESTART PROGRAM')
        input()
