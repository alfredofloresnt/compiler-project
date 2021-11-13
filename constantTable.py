import pprint

class ConstantsTable:
    def __init__(self):
        self.constants = {}

    def insert(self, name, address):
        self.constants[name] = {'name': name, 'address': address}

    def getConstantByName(self, name):
        if (name in self.constants):
            return self.constants[name]
        else:
            return None
    def getConstants(self):
        return self.constants
        
    def printConstantTable(self):
        pprint.pprint(self.constants)


        