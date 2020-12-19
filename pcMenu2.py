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
    2. [N]ew Part
    3. [M]ass enter sales
    4. [R]eceive new part shipment""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['1', 'f']:
                myPart = self.cli.search()
                if myPart is None:
                    continue
                self.partMenu(myPart)

            elif choice in ['3', 'm']:
                self.cli.massQtyChange('sell')
            elif choice in ['2', 'n']:
                self.newMenu()
            elif choice in ['4', 'r']:
                self.cli.massQtyChange('receive')

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
    1. [A]dd crossref
    2. [E]dit part fields
    3. [D]elete part 
    4. [B]ack to previous menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['1', 'a']:
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

    def newMenu(self):
        while True:
            print(
                """
======= NEW PART MENU =======
    1. [N]ew part
    2. [A]dd crossref to existing part
    4. [B]ack to previous menu""")
            choice = input('?')
            choice = choice[:1].lower()

            if choice in ['', '4', 'b']:
                return
            elif choice in ['2', 'a']:
                self.cli.addCrossRef()
            elif choice in ['1', 'n']:
                self.cli.newBin()


while True:
    try:
        p = pcMenu2()
        p.mainMenu()
    except:
        # raise
        pcCLI2.printYLW('ERROR: PROGRAM CRASHED. WRITE DOWN WHAT YOU JUST DID TO TELL TOM. 715-6827\n'
                        '  PRESS ENTER TO RESTART PROGRAM')
        input()
