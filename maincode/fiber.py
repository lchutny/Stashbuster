import itertools as it
import sys
import fileops

class Fiber():
    """ Class to store information on fibers"""
    def __init__(self, name, weight = 0, fibertype=None ):
        pass

    def add_fiber(self,name,weight,fibertype,choice):
        """adds fiber to database"""
        self.name = name
        self.weight = weight
        self.fibertype = fibertype
        self.choice = choice
        # Get current state of database:
        self.fiber_dict = self.recall()
        if choice == 'yarn':
            self.fiber_dict['yarn'][self.name] = {}
            self.update()
        elif choice == 'raw':
            self.fiber_dict['raw'][self.name] = {}
            print("Will add the raw fiber functions later")
        else:
            raise("Trouble adding fiber to database")

    def edit_fiber(self,edittype):
        """finds and edits fiber in database"""
        self.edittype = edittype
        self.fiber_dict = self.recall()
        print(self.fiber_dict)
        if self.edittype == 'yarn':
            fibers = sorted(self.fiber_dict['yarn'],key=str.lower)
            print("\nThis is your list of yarn(s) to edit:",*fibers, sep='\n')
            keepon = True
            while keepon:
                fiber_to_edit = input("Please type the name of the fiber you would like to edit: ")
                if fiber_to_edit in fibers:
                    self.name = fiber_to_edit
                    # set all the variables to the chosen fiber:
                    self.weight = self.fiber_dict['yarn'][self.name]['weight']
                    self.fibertype = self.fiber_dict['yarn'][self.name]['fibertype']
                    self.length = self.fiber_dict['yarn'][self.name]['length']
                    self.twist = self.fiber_dict['yarn'][self.name]['twist']
                    self.thickness = self.fiber_dict['yarn'][self.name]['thickness']
                    self.source = self.fiber_dict['yarn'][self.name]['source']
                    # Now actually call the update
                    self.update()
                    keepon = False
                else:
                    print("Try entering that fiber name again")
        elif self.edittype == 'raw':
            pass
        else:
            raise("Trouble editing fiber")


    def savestash(self,stashdict,stashname = 'Stash'):
        """always save as filename 'Stash' in this class"""
        s = fileops.FileOps()
        self.stashdict = stashdict
        self.stashname = stashname
        s.save_data(self.stashdict,self.stashname)

    def recall(self):
        """always recall filename 'Stash' in this class
        Yes this is hardcoded. At some point could improve this with a GUI
        Use this method to create the dictionary structure if it does not
        yet exist.
        """
        s1 = fileops.FileOps()
        stashname = 'Stash'
        stashdict = s1.recall_data(stashname)
        # If the dictionary is already set up (i.e. has keys), then continue.
        if stashdict.keys():
            return stashdict
        # If the dictionary keys are empty, create the dictionary.
        # Define Dictionary for projects
        # Layered Dictionary. First level keys are projecttypes
        # knitprojects, spinprojects or otherprojects
        # Next level keys are project names
        else:
            stashdict['yarn'] = {}
            stashdict['raw'] = {}
            return stashdict


class Yarn(Fiber):
    """Child Class of Fiber
    for more info on yarn thicknesses: https://www.craftyarncouncil.com/standards/yarn-weight-system
    """
    def __init__(self, length=0, twist=None, thickness=None, source=None):
        super().__init__(self)
        self.length = length
        self.twist = twist
        self.thickness = thickness
        self.source = source
        self._options = {'W':self.w,'F':self.f, 'L':self.lng, 'Z':self.z, 'T':self.t, 'S':self.s}

    def printyarn(self):
        """prints yarn"""
        print(f"\nYour yarn, {self.name}, is currently set to:\n\nweight:    {self.weight}\nFibertype: {self.fibertype}\nlength: {self.length}\ntwist: {self.twist}\nyarn thickness: {self.thickness}\nsource: {self.source}")

    def user_select(self):
        ud = input("\nW for weight(g), F for fibertype, L for length, Z for yarn twist, T for yarn thickness, S for source: ").upper()
        self.handle_options(ud)

    def handle_options(self,option):
        if option not in self._options:
            print("\nInvalid Entry - Please try again")
            # Reroute user to try again
            self.user_select()
        # Call the appropriate action for the option as chosen from the menu
        self._options[option]()

    def w(self):
        self.weight = int(input("Enter weight of yarn in g: "))
        if not self.weight >= 0:
            print("Weight will be set to zero")
            self.weight = 0

    def f(self):
        fibers =  {'W':'wool', 'A':'alpaca', 'S':'silk', 'C':'cotton', 'O':'other'}
        try:
            fib = input("Enter W for wool, A for alpaca, S for silk, C for cotton, O for other: ").upper()
            self.fibertype = fibers[fib]
            if self.fibertype == 'other':
                self.fibertype = input("Enter the type of fiber or blend: ")
        except:
            print("Incorrect Input, try again: ")
            self.f()

    def lng(self):
        self.length = float(input("\nEnter length of yarn in m: "))
        if not self.length > 0:
            print("Length will be set to zero")
            self.length = 0

    def z(self):
        twists = {'H':'high', 'M':'medium', 'L':'low'}
        try:
            tw = input("Enter L for low twist (like singles), M for medium, H for high (like sock): ").upper()
            self.twist = twists[tw]
        except:
            print("Incorrect Input, try again: ")
            self.z()

    def t(self):
        wts = {'F':'fingering', 'S':'sport', 'D':'DK', 'W':'worsted', 'C':'chunky', 'B':'bulky'}
        try:
            th = input("\nEnter F for Fingering/Sock, S for Sport/Baby, D for DK, W for Worsted/Aran, C for Chunky, B for Bulky: ").upper()
            self.thickness = wts[th]
            return self.thickness
        except:
            print("Incorrect Input, try again: ")
            self.t()

    def s(self):
        self.source = input("Enter source - store name or handspun: ")

    def update(self):
        """Asks user to update details of entry"""
        self.printyarn()
        try:
            contin = True
            while contin:
                ans = input("\nWould you like to update any of these? Y/N: ")
                if ans.upper() == 'Y':
                    self.user_select()
                else:
                    print("\nYou can always choose to edit the yarn later.")
                    contin = False
                    self.printyarn()
            self.file_yarn()
        except:
            raise ("\nError inputting updates")

    def file_yarn(self):
        self.fiber_dict['yarn'][self.name]['weight'] = self.weight
        self.fiber_dict['yarn'][self.name]['fibertype'] = self.fibertype
        self.fiber_dict['yarn'][self.name]['length'] = self.length
        self.fiber_dict['yarn'][self.name]['twist'] = self.twist
        self.fiber_dict['yarn'][self.name]['thickness'] = self.thickness
        self.fiber_dict['yarn'][self.name]['source'] = self.source
        print("Saving Fiber Data")
        self.savestash(self.fiber_dict)

    def yarn_selector(self, length, thickness):
        """Takes a length and a weight, queries the yarn stash and determines
        if a single yarn or combination of yarns can supply what is needed"""
        stashdict = self.recall()
        yarndict = stashdict['yarn']

        # # possible_yarns = []
        # # print(yarndict)
        # # print(yarndict['﻿Debbie BlissCashmerino ChunkyBlue']['weight'])
        # for yarn in yarndict:
        #     print(yarn['weight'])
        #     # if yarndict[yarn]['length'] >= length and yarndict[yarn]['thickness'] == thickness:
            #     possible_yarns.append(yarn)
        combos = self.combo_yarn(length,thickness)
        allyarns = sorted(possible_yarns) + sorted(combos)
        return allyarns

    def combo_yarn(self,length,thickness):
        """takes a desired yarn length and thickness and returns a list of tuples of two different yarn names that give the desired length and thickness when yarns held together

        Combos below from Kristin Tolle at https://orcasislandknitting.me/2017/10/21/key-for-two-yarns-together/ and from Lee Bernstein at http://www.knittingbrain.com/yarns.php
        """

        # First create lookup table for thicknesses:
        combinations = {'sport':('fingering','fingering'),'DK':('sport','sport'), 'worsted':('DK','DK'), 'chunky':('worsted', 'worsted'), 'bulky':('worsted','chunky')}
        combo = combinations[thickness]
        stashdict = self.recall()
        yarndict = stashdict['yarn']
        yarn1thk = combo[0]
        yarn2thk = combo[1]
        if yarn1thk == yarn2thk:
            # We are mixing two yarns of the same thickness
            possible_yarns = []
            for yarn in yarndict:
                if yarndict[yarn]['thickness'] == yarn1thk and yarndict[yarn]['length'] >= 2*length:
                    possible_yarns.append((yarn,yarndict[yarn]['length']))
            pairs = list(it.combinations(possible_yarns,2))
        else:
            possible_yarn1s = []
            possible_yarn2s = []
            for yarn in yarndict:
                if yarndict[yarn]['thickness'] == yarn1thk and yarndict[yarn]['length'] >= 2*length:
                    possible_yarn1s.append((yarn,yarndict[yarn]['length']))
                if yarndict[yarn]['thickness'] == yarn2thk and yarndict[yarn]['length'] >= 2*length:
                    possible_yarn2s.append((yarn,yarndict[yarn]['length']))
            pairs = list(it.product(possible_yarn1s,possible_yarn2s))
        return pairs

    def possible_project(yarn):
        """takes a yarn from stash and determines what possible projects
        can be made from it - returns a list"""
        pass

class RawFiber(Fiber):
    """Child class of Fiber"""
    def __init__(self,raw_fiber_type=None,prep=None):
        super().__init__(self)
        self.raw_fiber_type = raw_fiber_type # (Combed Top, Roving, Rolag)
        self.prep = prep # (worsted or woolen)
