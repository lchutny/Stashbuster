import pickle

class FileOps():
    """Save and retrieve data"""

    def __init__(self):
        pass

    def save_data(self,to_save,data_type):
        """generic save function to save stash, project or tool data
        to file. to_save is a dictionary of projects, tools or stash
        """
        self.dict_to_save = to_save
        self.data_type = str(data_type)
        with open(self.data_type,'wb') as f:
            pickle.dump(self.dict_to_save,f)

    def recall_data(self, data_type):
        self.data_type = data_type
        try:
            with open(self.data_type,'rb') as f1:
                return pickle.load(f1)
        except FileNotFoundError:
            dict_1 = {}
            with open(self.data_type, 'wb') as f2:
                pickle.dump(dict_1,f2)
                return dict_1
        else:
            raise ("can't find file to read from")
