import fiber
import tools
import fileops
import sys


class Project():
    """Class to create and store information on projects"""

    def __init__(self):
        pass

    def add_project(self,name,projtype):
        """adds new project to database"""
        self.name = name
        self.projtype = projtype
        # Get current state of database:
        self.project_dict = self.recall()
        # Add Project to database:
        if self.projtype == 'knit':
            self.project_dict['knitprojects'][self.name] = {}
            self.update()
        elif self.projtype == 'spin':
            self.project_dict['spinprojects'][self.name] = {}
            print("Remaining Spin Project functionality under construction")
        elif self.projtype == 'other':
            self.project_dict['otherprojects'][self.name] = {}
            print("Remaining Other Project functionality under construction")
        else:
            raise ("Trouble adding to database")

    def edit_project(self,edittype):
        """finds and edits project in database
        Includes updates to supply amounts
        includes way to close project and archive
        """
        self.edittype = edittype
        self.project_dict = self.recall()
        if self.edittype == 'knit':
            projects = sorted(self.project_dict['knitprojects'],key=str.lower)
            print("\nThis is your list of projects to edit:",*projects,sep='\n')
            keepon = True
            while keepon:
                proj_to_edit = input("\nPlease type in the name of the proejct you would like to edit: ")
                if proj_to_edit in projects:
                    self.name = proj_to_edit
                    # set all the variables to the chosen project:
                    self.category =      self.project_dict['knitprojects'][self.name]['category']
                    self.len_reqd = self.project_dict['knitprojects'][self.name]['length']
                    self.size = self.project_dict['knitprojects'][self.name]['size']
                    self.yarn_thickness = self.project_dict['knitprojects'][self.name]['thickness']
                    self.yarn_twist = self.project_dict['knitprojects'][self.name]['twist']
                    self.yarn_fibertype = self.project_dict['knitprojects'][self.name]['fibertype']
                    self.special_technique = self.project_dict['knitprojects'][self.name]['technique']
                    # Now update
                    self.update()
                    keepon = False
                else:
                    print("Try entering that project name again.")
        elif self.edittype == 'spin':
            pass
        elif self.edittype == 'other':
            pass
        else:
            raise ("Trouble editing project")

    def tool_reqt(self,tooltype,toolsize):
        """queries tool database for required tools - for future"""
        pass

    def savedata(self,datadict,dataname = 'Projects'):
        """always save as filename 'Projects' in this class"""
        s = fileops.FileOps()
        self.datadict = datadict
        self.dataname = dataname
        s.save_data(self.datadict,self.dataname)

    def recall(self):
        """always recall filename 'Projects' in this class
        Yes this is hardcoded. At some point could improve this with a GUI
        Use this method to create the dictionary structure if it does not
        yet exist.
        """
        s1 = fileops.FileOps()
        dataname = 'Projects'
        datadict = s1.recall_data(dataname)
        # If the dictionary is already set up (i.e. has keys), then continue.
        if datadict.keys():
            return datadict
        # If the dictionary keys are empty, create the dictionary.
        # Dictionary for projects is a Layered Dictionary.
        # First level keys are projecttypes:
        #            knitprojects, spinprojects or otherprojects
        # Next level keys are project names
        else:
            datadict['knitprojects'] = {}
            datadict['spinprojects'] = {}
            datadict['otherprojects'] = {}
            return datadict


class KnitProject(Project):
    """child class of project for knitting projects."""

    def __init__(self,category=None,len_reqd=0,size=None):
        super().__init__()
        self.category = category # hat, shawl, scarf, etc.
        self.len_reqd = len_reqd
        self.size = size # Baby, Child, Adult
        self.yarn_thickness = None #lace, DK, Worsted, etc.
        self.yarn_twist = None
        self.yarn_fibertype = None # Wool, silk, alpaca, etc
        self.special_technique = None
        self.yarn_choice = None
        self._options = {'C': self.c, 'L':self.l, 'S':self.s, 'T':self.t, 'W':self.w, 'F':self.f, 'U':self.u}

    def printproject(self):
        """prints project"""
        print(f"\nYour project, {self.name}, is currently set to:\n\ncategory:    {self.category}\nRequired length: {self.len_reqd}\nsize: {self.size}\nyarn thickness: {self.yarn_thickness}\nyarn twist: {self.yarn_twist}\nfiber type: {self.yarn_fibertype}\nspecial techniques: {self.special_technique}\nyarn choice: {self.yarn_choice}")

    def user_select(self):
        ud = input("\nC for category, L for length, S for size, T for yarn thickness, W for yarn twist, F for fiber type, U for special techniques: ").upper()
        self.handle_options(ud)

    def handle_options(self,option):
        if option not in self._options:
            print("Invalid Entry - Please try again")
            # Reroute user to try again
            self.user_select()
        # Call the appropriate action for the option as chosen from the menu
        self._options[option]()

    def c(self):
        cats = {'H':'Hat', 'S':'Shawl', 'F':'Scarf', 'W':'Sweater', 'M':'Mittens', 'K':'Socks', 'C':'Cowl'}
        try:
            cat = input("\nEnter H for hat, S for Shawl, F for Scarf, W for Sweater, M for mittens, K for Socks or C for Cowl: ").upper()
            self.category = cats[cat]
            return
        except:
            print("\nIncorrect Input, try again: ")
            self.c()

    def l(self):
        self.len_reqd = int(input("\nEnter length of yarn required to complete project in m: "))
        if not self.len_reqd >= 0:
            print("Length will be set to zero")
            self.len_reqd = 0

    def s(self):
        sizes = {'B':'baby', 'C':'child', 'A':'adult'}
        try:
            sz = input("\nEnter B for baby, C for child, A for adult: ").upper()
            self.size = sizes[sz]
        except:
            print("\nIncorrect Input, try again: ")
            self.s()

    def t(self):
        wts = {'F':'fingering', 'S':'sport', 'D':'DK', 'W':'worsted', 'C':'chunky', 'B':'bulky'}
        try:
            th = input("\nEnter F for Fingering/Sock, S for Sport/Baby, D for DK, W for Worsted/Aran, C for Chunky, B for Bulky: ").upper()
            self.yarn_thickness = wts[th]
            return self.yarn_thickness
        except:
            print("\nIncorrect Input, try again: ")
            self.t()

    def w(self):
        twists = {'L':'lowtwist', 'M':'medtwist', 'H':'hightwist'}
        try:
            tw = input("\nEnter L for low twist (like singles), M for medium, H for high (like sock): ").upper()
            self.yarn_twist = twists[tw]
        except:
            print("\nIncorrect Input, try again: ")
            self.w()

    def f(self):
        fibers = {'W':'wool', 'A':'alpaca', 'S':'silk', 'C':'cotton', 'O':'other'}
        try:
            fib = input("\nEnter W for wool, A for alpaca, S for silk, C for cotton, O for other: ").upper()
            self.yarn_fibertype = fibers[fib]
            if self.yarn_fibertype == 'other':
                self.yarn_fibertype = input("Enter the type of fiber or blend: ")
        except:
            print("\nIncorrect Input, try again: ")
            self.f()

    def u(self):
        self.special_technique = input("\nEnter any special tecnique: ")

    def update(self):
        """Asks user to update details of entry"""
        self.printproject()
        try:
            contin = True
            while contin:
                ans = input("\nWould you like to update any of these? Y/N: ")
                if ans.upper() == 'Y':
                    self.user_select()
                else:
                    print("\nYou can always choose to edit the project later.")
                    self.printproject()
                    contin = False
            con = True
            while con:
                ans = input("\nWould you like to choose a yarn for this project? Y/N: ").upper()
                if ans == 'Y':
                    if self.len_reqd == 0 or self.yarn_thickness == None:
                        print("Please input a length and yarn thickness at a minimum")
                        self.update()
                    length = self.len_reqd
                    thickness = self.yarn_thickness
                    self.file_project()
                    self.yarn_choice = self.stash_yarn_reqt(length,thickness)
                    con = False
                elif ans == 'N':
                    con = False
                    break
                else:
                    ("\nIncorrect entry, choose Y/N")
            self.file_project()
        except:
            raise ("Error inputting updates")

    def file_project(self):
        self.project_dict['knitprojects'][self.name]['category'] = self.category
        self.project_dict['knitprojects'][self.name]['length'] = self.len_reqd
        self.project_dict['knitprojects'][self.name]['size'] = self.size
        self.project_dict['knitprojects'][self.name]['thickness'] = self.yarn_thickness
        self.project_dict['knitprojects'][self.name]['twist'] = self.yarn_twist
        self.project_dict['knitprojects'][self.name]['fibertype'] = self.yarn_fibertype
        self.project_dict['knitprojects'][self.name]['technique'] = self.special_technique
        self.project_dict['knitprojects'][self.name]['yarnchoice'] = self.yarn_choice
        # Create a savefile instance and call the file save method:
        print("\nSaving project data\n")
        self.savedata(self.project_dict)

    def stash_yarn_reqt(self,length,thick):
        """query yarn stash to see if reqd yarn available
        return name of yarn that matches or None if none in stash
        THis function should only pass the required yarn length and yarn_thickness to the fiber class which returns possible named yarns in a list
        """
        y = fiber.Yarn()
        yarns_avail = y.yarn_selector(length,thick)
        if len(yarns_avail) > 0:
            print(f"\nFor project {self.name}, you could use:")
            print([yarn for yarn in yarns_avail])
            choice = input("\nPlease select name of yarn for this project: ")
            if choice in yarns_avail:
                return choice
            else: # Select a default yarn
                return yarns_avail[0]
            print("\nAnd don't forget to swatch!!")
        else:
            print("\nYou need to add some yarns to the stash! There's nothing to choose from at the moment.")
            return None

    def new_yarn(self,yarn_reqd):
        """if no stash yarn available, scrape the web for yarn options,
        return list of options with prices
        """
        pass


class SpinProject(Project):
    """child class of project for spinning projects."""

    def __init__(self,raw_fiber=None):
        self.raw_fiber = raw_fiber # hat, shawl, scarf, etc.
        self.singles = True
        self.plies = 0 #
        self.singles_twist = 'Z'
        self.plied_twist = 'S' # Wool, silk, alpaca, etc
        self.spin_type = None #Worsted, semi-worsted or woolen


class OtherProject(Project):
    """child class of project for other fiber related projects (e.g.
    tatting, crocheting, needle felting, etc.
    """
    # FOR FUTURE
    def __init__(self):
        pass
