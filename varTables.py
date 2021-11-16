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

import pprint

class Vars:
    def __init__(self):
        self.items = {}
    def insert(self, item):
        self.items[item["name"]] = item
    def getVariableByName(self, name):
        if (name in self.items):
            return self.items[name]
        return None
    def getSize(self):
        return len(self.items)
    def printVars(self):
        pprint.pprint(self.items)

class Params:
    def __init__(self):
        self.items = []
    def insert(self, item):
        self.items.append(item)
    def getParamByIndex(self, index):
        # Check if points to null
        if (index <= len(self.items) - 1):
            return self.items[index]
        else:
            return None
    def getSize(self):
        return len(self.items)
    def printParams(self):
        pprint.pprint(self.items)

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
    def addParametersTable(self, name, data):
        if (name in self.dirFuncData):
            self.dirFuncData[name]["parameterTable"] = data
            return self.dirFuncData[name]["parameterTable"]
        else:
            return None
    def getVarsTableByFunctionName(self, name):
        if (name in self.dirFuncData):
            return self.dirFuncData[name]["table"]
    def setTotParameters(self, name, val):
        self.dirFuncData[name]["totParameters"] = val
    def setTotLocalVars(self, name, val):
        self.dirFuncData[name]["totLocalVars"] = val - self.dirFuncData[name]["totParameters"]
    def setCountQuadruples(self, name, val):
        self.dirFuncData[name]["startAtQuad"] = val 
    def getStartAtQuad(self, name):
        return self.dirFuncData[name]["startAtQuad"]
    def getMainName(self):
        return list(self.dirFuncData.keys())[0]
    def printDirFunc(self):
        pprint.pprint(self.dirFuncData)

class ArrayDimNode:
    def __init__(self):
        self.nDim = 1
        self.limInf = None
        self.limSup = None
        self.m = 0
        self.nextNode = None
    def setNextNode(self, node):
        self.nextNode = node
    def setLimInf(self, val):
        self.limInf = val
    def setLimSup(self, val):
        self.limSup = val
    def addDim(self):
        self.nDim += 1
    def setM(self, val):
        self.m = val
    def getLimInf(self):
        return self.limInf
    def getLimSup(self):
        return self.limSup
    def getNextNode(self):
        return self.nextNode
    def printNode(self):
        print("Node", self.nDim, "limInf", self.limInf, "limSup", self.limSup, "nextNode", self.nextNode)



#class MyFuncTables:

def getFunctionByName(arr, value):
    for item in arr:
        if (item["name"] == value):
            return item
    return None

#getFunctionByName(dirFunc, "134")["table"].insert("test")
#getFunctionByName(dirFunc, "asdasd")["table"].printVars()