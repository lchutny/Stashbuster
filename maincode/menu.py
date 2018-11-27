import fiber
import project
import tools
import fileops
import sys


def possible_project(self):
    pass

class Menu():
    """Allows selection of methods and running of the program 'Stashbuster'
    """

    print("Welcome to Stashbuster!\n\nYour selections are:\n\nP to add or edit project\nF to add or edit fiber (yarn or raw fiber)\nT to add or view tools\nQ to quit")

    def __init__(self):
        """define top level menu options as private variable"""
        self._options = {'P':self.project, 'F':self.fiber, 'T':self.tools, 'Q':self.quitprogram}

    def user_select(self):
        """get input from user and call handling method"""
        option = input("\nPlease enter an action (P (project), F(fiber), T(tool), Q(quit)): ").upper()
        self.handle_options(option)

    def handle_options(self, option):
        if option not in self._options:
            print("Invalid Entry - Please try again")
            # Reroute user to try again
            self.user_select()
        # Call the appropriate action for the option as chosen from the menu
        self._options[option]()

    def project(self):
        # Open the Project Sub Menu and get user selection
        p = ProjSubMenu()
        p.user_select()

    def fiber(self):
        f = FiberSubMenu()
        f.user_select()

    def tools(self):
        t = ToolSubMenu()
        t.user_select()

    def quitprogram(self):
        print("Thanks for using Stashbuster")
        sys.exit()


class ProjSubMenu(Menu):
    """ Sub menu for Projects """
    def __init__(self):
        Menu.__init__(self)
        self._options = {'N':self.new_project, 'E':self.edit_project, 'Q':self.quitprogram}

    def user_select(self):
        option = input("\nEnter N for new or E to edit a project (Q to quit): ").upper()
        self.handle_options(option)

    def new_project(self):
        """instantiates a new project"""
        try:
            newname = input("\nEnter a name for your new project: ")
            pt = ProjTypeMenu()
            pt.user_select(newname,'new')
            print("New project successfully created")
            # Go back to main menu once done
            # super().user_select()  (NOT WORKING)
        except:
            print("\nTrouble creating new project")

    def edit_project(self):
        """allows editing of existing project"""
        try:
            projname = None  #Use an empty name so we can use the same method
            pte = ProjTypeMenu()
            pte.user_select(projname,'edit')
            # Go back to main menu once done
            # super().user_select() NOT WORKING
        except:
            print("\nTrouble editing project")


class ProjTypeMenu(Menu):
    """Sub Menu under projects for choosing knitting spinning or
    other projects
    """

    def __init__(self):
        Menu.__init__(self)
        self._options = {'K':self.knit_project, 'S':self.spin_project, 'O':self.other_project,'Q':self.quitprogram}

    def user_select(self,name,action):
        self.newname = name
        self.action = action
        option = input("\nEnter K for Knit project, S for Spinning or O for other (Q to quit): ").upper()
        self.handle_options(option)

    def knit_project(self):
        if self.action == 'new':
            p = project.KnitProject()
            p.add_project(self.newname,'knit')
        elif self.action == 'edit':
            p = project.KnitProject()
            p.edit_project('knit')

    def spin_project(self):
        if self.action == 'new':
            p = project.SpinProject()
            p.add_project(self.newname,'spin')
        elif self.action == 'edit':
            p = project.SpinProject()
            p.edit_project('spin')

    def other_project(self):
        if self.action == 'new':
            p = project.OtherProject()
            p.add_project(self.newname,'other')
        elif self.action == 'edit':
            p = project.OtherProject()
            p.edit_project('other')


class FiberSubMenu(Menu):
    """Sub menu for Fiber tasks"""
    def __init__(self):
        Menu.__init__(self)
        self._options = {'N':self.new_fiber, 'E':self.edit_fiber, 'I':self.query_inventory, 'Q':self.quitprogram}

    def user_select(self):
        option = input("\nEnter N for new, E to edit a fiber or I to query inventory (Q to quit): ").upper()
        self.handle_options(option)

    def new_fiber(self):
        """instantiates new fiber"""
        try:
            newname = input("\nEnter a name for your new fiber: ")
            fibwt = int(input("\nEnter weight of fiber/yarn in g: "))
            fibtype = input("\nEnter fiber/yarn type: W for wool, A for alpaca, S for silk, C for cotton, O for other: ").upper()
            ft = FiberTypeMenu()
            ft.user_select(newname, fibwt, fibtype, 'new')
            print("\nNew fiber successfully created")
        except:
            print("\nTrouble creating new fiber")

    def edit_fiber(self):
        """for editing an existing fiber"""
        try:
            #Use empty variables so we can use the same method
            fibername = None
            fibwt = 0
            fibtype = None
            fte = FiberTypeMenu()
            fte.user_select(fibername, fibwt, fibtype, 'edit')
        except:
            print("Trouble editing fiber")

    def query_inventory(self):
        """Runs yarn selector in fiber"""
        f = fiber.Yarn()
        length = int(input("\nInput length desired: "))
        print("\nInput thickness of yarn desired: ")
        thickness = f.t()
        yarns_avail = f.yarn_selector(length,thickness)
        print("\nMatching yarns are:")
        print([yarn for yarn in yarns_avail])


class FiberTypeMenu(Menu):
    """Sub Menu under fiber for choosing yarn or rawfiber"""

    def __init__(self):
        Menu.__init__(self)
        self._options = {'Y':self.yarn, 'R':self.raw_fiber, 'Q':self.quitprogram}

    def user_select(self, name, fibwt, fibtype, action):
        self.newname = name
        self.weight = fibwt
        self.fibertype = fibtype
        self.action = action
        option = input("\nEnter Y for Yarn, R for Raw fiber (Q to quit): ").upper()
        self.handle_options(option)

    def yarn(self):
        if self.action == 'new':
            y = fiber.Yarn()
            y.add_fiber(self.newname,self.weight,self.fibertype,'yarn')
        elif self.action == 'edit':
            y = fiber.Yarn()
            y.edit_fiber('yarn')

    def raw_fiber(self):
        if self.action == 'new':
            r = fiber.RawFiber()
            r.add_fiber(self.newname,self.weight,self.fibertype,'raw')
        elif self.action == 'edit':
            r = fiber.RawFiber()
            y.edit_fiber('raw')


class ToolSubMenu(Menu):
    """Sub menu for Tool Tasks"""
    def __init__(self):
        Menu.__init__(self)
        self._options = {'N':self.new_tool, 'V':self.view_tool, 'Q':self.quitprogram}

    def user_select(self):
        option = input("\nEnter N for new or V to view tool inventory (Q to quit): ").upper()
        self.handle_options(option)

    def new_tool(self):
        """creates new tool"""
        try:
            tt = ToolTypeMenu()
            tt.user_select('new')
            print("\nNew tool successfully created")
        except:
            print("\nTrouble creating new tool")

    def view_tool(self):
        """prints existing tool list"""
        try:
            tte = tools.Tools()
            tte.view_tools()
        except:
            print("\nTrouble viewing tools")


class ToolTypeMenu(Menu):
    "Sub menu for choosing type of tool"

    def __init__(self):
        Menu.__init__(self)
        self._options = {'S':self.straights, 'C':self.circulars, 'D':self.dpns,'H':self.hook, 'Q':self.quitprogram}

    def user_select(self,action):
        self.action = action
        option = input("\nEnter S for straight knitting needles, C for Circulars, D for DPNs or H for Crochet Hook (Q to quit): ").upper()
        self.handle_options(option)

    def straights(self):
        if self.action == 'new':
            t = tools.Tools()
            t.add_tool('straights')

    def circulars(self):
        if self.action == 'new':
            t = tools.Tools()
            t.add_tool('circulars')

    def dpns(self):
        if self.action == 'new':
            t = tools.Tools()
            t.add_tool('dpns')

    def hook(self):
        if self.action == 'new':
            t = tools.Tools()
            t.add_tool('hook')



# This instantiates the Menu class which is used to
# run the program and opens the menu selector
runprog = Menu()
runprog.user_select()
