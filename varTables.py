#class Node:
#    def __init__(self):
#        self.items = []
#        self.nextval = None
#    def insert(self, item):
#        self.items.append(item)
#    def printQueue(self):
#        print(self.items)
#
#class MyFuncTables:
#    def __init__(self):
#        self.headval = None
#    def listprint(self):
#      printval = self.headval
#      while printval is not None:
#         print (printval.items)
#         printval = printval.nextval
#
#        
#
#list1 = MyFuncTables()
#dirFun = Node()
#dirFun.insert({"name": "asdasd", "type": 1})
#dirFun.insert({"name": "qweqwe", "type": 2})
#list1.headval = dirFun
#vars1 = Node()
#vars1.insert({"name": "dfgdfg", "type": 3})
#list1.headval.nextval = vars1
#
## Link second Node to third node
##e2.nextval = e3
#
#list1.listprint()

class Vars:
    def __init__(self):
        self.items = {}
    def insert(self, item):
        self.items[item["name"]] = item
    def getVariableByName(self, name):
        if (name in self.items):
            return self.items[name]
        return None
    def printVars(self):
        print(self.items)

class DirFunc:
    def __init__(self):
        self.dirFuncData = {}
    def insert(self, item):
        self.dirFuncData[item["name"]] = item
    def getFunctionByName(self, name):
        if (name in self.dirFuncData):
            return self.dirFuncData[name]
        return None
    def addVarsTable(self, name, data):
        if (name in self.dirFuncData):
            self.dirFuncData[name]["table"] = data
            return self.dirFuncData[name]["table"]
        else:
            return None
    def getVarsTableByFunctionName(self, name):
        if (name in self.dirFuncData):
            return self.dirFuncData[name]["table"]
        return None
    def printDirFunc(self):
        print(self.dirFuncData)
    

#class MyFuncTables:

def getFunctionByName(arr, value):
    for item in arr:
        if (item["name"] == value):
            return item
    return None

#getFunctionByName(dirFunc, "134")["table"].insert("test")
#getFunctionByName(dirFunc, "asdasd")["table"].printVars()