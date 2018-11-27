from collections import defaultdict
import fileops
import sys

class Tools():
    """ Class to store and manage all fiber related tools
    need to add methods to edit and query tools
    """

    def __init__(self):
        pass

    def add_tool(self,tooltype=None):
        """adds new tools to database"""
        self.tool_dict = self.recall()
        self.tooltype = tooltype
        if self.tooltype == 'hook':
            contin = True
            while contin:
                sizetype = input("\nPlease indicate if hook size is U for US., K for UK or M for mm: ").upper()
                if sizetype == 'U':
                    ussize = input("\nPlease enter US size number - B-T: ").upper()
                    self.mm_size = self.converthook('US',ussize)
                    contin = False
                elif sizetype == 'K':
                    uksize = (input("\nPlease enter UK size number - 14 - 000: "))
                    self.mm_size = self.converthook('UK',uksize)
                    contin = False
                elif sizetype == 'M':
                    self.mm_size = float(input("\nPlease enter size in mm: ")) # in mm
                    contin = False
                else:
                    print("\nPlease enter U, K or M: ")
        else:
            contin1 = True
            while contin1:
                sizetype = input("\nPlease indicate if size is U for US, K for UK or M for mm: ").upper()
                if sizetype == 'U':
                    ussize = float(input("\nPlease enter US size number - 0-50: "))
                    self.mm_size = self.convert('US',ussize)
                    contin1 = False
                elif sizetype == 'K':
                    uksize = (input("\nPlease enter UK size number - 000 to 14: "))
                    self.mm_size = self.convert('UK',uksize)
                    contin1 = False
                elif sizetype == 'M':
                    self.mm_size = float(input("\nPlease enter size in mm: "))
                    contin1 = False
                else:
                    print("\nPlease enter U, K or M: ")
        self.file_tool()

    def view_tools(self):
        """Method to show all tools available in inventory"""
        self.tool_dict = self.recall()
        print("The tool library is:")
        print(self.tool_dict)
        # Need to put in a prettier way to print this


    def convert(self,type,size):
        """ Converts UK and US needles sizes and returns  mm. Courtesy Vogue Knitting.
        Tuple of tuples with (US,UK,mm)
        Set up so that 3 way conversions could eventually be done
        """
        sizes = ((0,14,2), (1,13,2.25), (2,12,2.75), (None,11,3), (3,10,3.25), (4,None,3.5), (5,9,3.75), (6,8,4), (7,7,4.5), (8,6,5), (9,5,5.5), (10,4,6), (10.5,3,6.5), (None,2,7), (None,1,7.5), (11,0,8), (13,'00',9), (15,'000',10), (17,None,12), (19,None,16), (35,None,19), (50,None,25))
        if type == 'US':
            for s in sizes:
                if s[0] == size:
                    mm = s[2]
        else: # for UK sizes
            for s in sizes:
                if s[1] == size:
                    mm = s[2]
        return mm

    def converthook(self,type,size):
        """ Converts UK and US crochet hook sizes and returns mm. Courtesy Mary Maxim.
        Tuple of tuples with (US,UK,mm)
        Set up so that 3 way conversions could eventually be done
        """
        sizes = ((None,14,2), ('B-1',13,2.25), ('C-2',12,2.75), (None,11,3), ('D-3',10,3.25), ('E-4',9,3.5), ('F-5',None,3.75), ('G-6',8,4), (7,7,4.5), ('H-8',6,5), ('I-9',5,5.5), ('J-10',4,6), ('K-10.5',3,6.5), (None,2,7), ('L-11',0,8), ('M-13','00',9), ('N-15','000',10), ('P-15',None,15), ('Q',None,16), ('S',None,19), ('T',None,30))
        if type == 'US':
            for s in sizes:
                if s[0] == size:
                    mm = s[2]
        else: # for UK sizes
            for s in sizes:
                if s[1] == size:
                    mm = s[2]
        return mm

    def file_tool(self):
        if self.tooltype == 'straights':
            self.tool_dict['straights'][self.mm_size] += 1
        elif self.tooltype == 'circulars':
            self.tool_dict['circulars'][self.mm_size] += 1
        elif self.tooltype == 'dpns':
            self.tool_dict['dpns'][self.mm_size] += 1
        else:
            self.tool_dict['hook'][self.mm_size] += 1
        print("\nSaving Tool Data")
        self.savedata(self.tool_dict)

    def savedata(self,datadict,dataname = 'Tools'):
        """always save as filename 'Tools' in this class"""
        s = fileops.FileOps()
        self.datadict = datadict
        self.dataname = dataname
        s.save_data(self.datadict,self.dataname)

    def recall(self):
        """always recall filename 'Tools' in this class
        Yes this is hardcoded. At some point could improve this with a GUI
        Use this method to create the dictionary structure if it does not
        yet exist.
        """
        s1 = fileops.FileOps()
        dataname = 'Tools'
        datadict = s1.recall_data(dataname)
        # If the dictionary is already set up (i.e. has keys), then continue.
        if datadict.keys():
            return datadict
        # If the dictionary keys are empty, create the dictionary.
        # Dictionary for projects is a Layered Dictionary.
        # First level keys are tool types: straights, circulars
        # DPNs and crochet hooks
        # Next level keys are dictionaries starting at 0 to automatically
        # add the size as the key value and allow counting/incrementing the
        # inventory
        else:
            datadict['straights'] = defaultdict(int)
            datadict['circulars'] = defaultdict(int)
            datadict['dpns'] = defaultdict(int)
            datadict['hook'] = defaultdict(int)
            return datadict
