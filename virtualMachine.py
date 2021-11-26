import pprint
import quadruples as qp
from errorHandler import Error
import pickle
import statistics
import matplotlib.pyplot as plt

# Memory definition
class Memory():
    def __init__(self):
        self.data = {}
    def insert(self, address, value):
        self.data[address] = value
    def get(self, address):
        if (address in self.data):
            return self.data[address]
        else:
            raise Exception('"Runtime error: Variable not found')
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def printMemory(self):
        pprint.pprint(self.data)

# Stack segment definition
class StackSegment():
    def __init__(self):
        self.data = [{}]
        self.tempLocalMemory = [{}] 
    def insertNewMemState(self):
        self.data.append({})
        self.tempLocalMemory.append({})
    def insertTop(self, address, val):
        self.data[len(self.data)-1][address] = val
    def insertTopTemp(self, address, val):
        self.tempLocalMemory[len(self.tempLocalMemory)-1][address] = val
    def get(self, address):
        if (address in self.data):
            return self.data[address]
        else:
            Error("Runtime error: Variable not found")
    def getPreviousState(self, address):
        if (address in self.data[len(self.data)-2]):
            return self.data[len(self.data)-2][address]
        else:
            return None
    def getPreviousStateTemp(self, address):
        if (address in self.tempLocalMemory[len(self.tempLocalMemory)-2]):
            return self.tempLocalMemory[len(self.tempLocalMemory)-2][address]
        else:
            return None
    def getTop(self, address):
        if (address in self.data[len(self.data)-1]):
            return self.data[len(self.data)-1][address]
        else:
            return None
    def getTopTemp(self, address):
        if (address in self.tempLocalMemory[len(self.tempLocalMemory)-1]):
            return self.tempLocalMemory[len(self.tempLocalMemory)-1][address]
        else:
            return None
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def getTempLocalMem(self):
        return self.tempLocalMemory
    def getDataPrev(self):
        return self.data[len(self.data)-2]
    def popStack(self):
        self.data.pop()
        self.tempLocalMemory.pop()
    def printMemory(self):
        for x in self.data:
            pprint.pprint(x)


# Vistual machine definition. All the operations from generated quadruples are executed here.
class VirtualMachine():
    def beginMachine(self):
        objectCodeData = None
        with open('object.code', 'rb') as handle:
            objectCodeData = pickle.load(handle)
        dirFunc = objectCodeData["dirFunc"]
        constantsTable = objectCodeData["constantsTable"]
        quadruples = objectCodeData["quadruples"]
        def insertInMemory(address, value):
            if (address >= 1000 and address <= 3999):
                globalMemory.insert(address, value)
            elif (address >= 4000 and address <= 6999):
                localMemory.insertTop(address, value)
            elif (address >= 7000 and address <= 8499):
                tempGlobalMemory.insert(address, value)
            elif (address >= 8500 and address <= 9999):
                localMemory.insertTopTemp(address, value)
            elif (address >= 10000 and address <= 12999):
                constantsMemory.insert(address, value)
        def getFromMemory(address):
            if (address >= 1000 and address <= 3999):
                return globalMemory.get(address)
            elif (address >= 4000 and address <= 6999):
                if localMemory.getTop(address) != None:
                    return localMemory.getTop(address)
                else:
                    return localMemory.getPreviousState(address)
            elif (address >= 7000 and address <= 8499):
                return tempGlobalMemory.get(address)
            elif (address >= 8500 and address <= 9999):
                if localMemory.getTopTemp(address) != None:
                    return localMemory.getTopTemp(address)
                else:
                    return localMemory.getPreviousStateTemp(address)
            elif (address >= 10000 and address <= 12999):
                return constantsMemory.get(address)
        def getLocalOrGlobal(address):
            if (localMemory.getPreviousState(address)):
                return localMemory.getPreviousState(address)
            elif (globalMemory.get(address)):
                return globalMemory.get(address)
        def isAddressPointer(address):
            if (str(address)[0] == '(' and str(address)[-1] == ')'):
                address = int(address[1:-1])
                return address
            else:
                return None
        def notAddress(address):
            if (str(address)[0] == '*'):
                return int(address[1:])
            else:
                return None
        def getTransformmedAddress(address, index = 0):
            if (notAddress(address)):
                return notAddress(address)
            elif (isAddressPointer(address)):
                pointer = isAddressPointer(address)
                if (index == 3):
                    return getFromMemory(pointer)
                return getFromMemory(getFromMemory(pointer))
            else:
                if (index == 3):
                    return address
                return getFromMemory(address)
        def findVariableByAdrresInDir(address, currentFunc):
            variables = dirFunc.getVarsTableByFunctionName(currentFunc).getData()

            for key, obj in variables.items():
                print(obj, address)
                if (obj["address"] == address):
                    return obj
            return None
        # Memory initialization
        globalMemory = Memory()
        localMemory = StackSegment()
        checkpoints = qp.Stack()
        #tempLocalMemory = Memory()
        tempGlobalMemory = Memory()
        constantsMemory = Memory()

        # Variables initialization
        ip = 0
        paramsStore = []
        currentQuad = quadruples.get(ip)
        currentFunc = dirFunc.getMainName()

        # Change keys to address to get quick access
        for key, obj in constantsTable.items():
            constantsMemory.insert(obj['address'], obj['name'])

        while(currentQuad[0] != 'END'): # Ends program when a END is found
            currentQuad = quadruples.get(ip)
            # Big switch case
            if (currentQuad[0] == '='): # Assignation is found
                newVal = getTransformmedAddress(currentQuad[1])
                resDir = getTransformmedAddress(currentQuad[3], 3)
                insertInMemory(resDir, newVal)
            if (currentQuad[0] == '+'): # addition is founds
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft + valRight)
            if (currentQuad[0] == '-'): # Substraction is found
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft - valRight)
            if (currentQuad[0] == '*'): # Mult is found
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft * valRight)
            if (currentQuad[0] == '/'): # Division is found
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft / valRight)
            if (currentQuad[0] == 'GoTo'): # GOTO id found
                ip = currentQuad[3] - 2 # -2 Because quads start at index 0 and add one more iteration
            if (currentQuad[0] == 'GoToF'):
                val = getTransformmedAddress(currentQuad[1])
                if (val == 0):
                    ip = currentQuad[3] - 2
            if (currentQuad[0] == '<'):# Less than id found
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft < valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '>'): # Greater than is found
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft > valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '>='):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft >= valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '<='):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft <= valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '!='):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft != valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '=='):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '&&'):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == 1 and valRight == 1):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '||'):
                valLeft = getTransformmedAddress(currentQuad[1])
                valRight = getTransformmedAddress(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == 1 or valRight == 1):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == 'PRINT'):
                val = getFromMemory(getTransformmedAddress(currentQuad[3], 3))
                print(val)
            if (currentQuad[0] == 'READ'):
                varToBeAssigned = currentQuad[1]
                val = input()
                # Return the type of a string that can be converted in other type 
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        val = str(val)[0]
                        return "char"
                insertInMemory(varToBeAssigned, val)
            if (currentQuad[0] == 'ERA'):
                #Validate space
                paramsStore = []
                localMemory.insertNewMemState()
                for key, obj in dirFunc.getFunctionByName(currentQuad[1])['table'].getData().items():
                    paramsStore.append({'name': obj['name'], 'address': obj['address'], 'type': obj['type']})
            if (currentQuad[0] == 'PARAMETER'):
                paramIndex = currentQuad[3]-1
                address = paramsStore[paramIndex]['address']
                val = getTransformmedAddress(currentQuad[1])
                insertInMemory(address, val)
            if (currentQuad[0] == 'GOSUB'):
                saveQuad = ip + 2
                checkpoints.push(saveQuad)
                currentFunc = currentQuad[1]
                needReturn = True if dirFunc.getFunctionByName(currentFunc)['type'] != "void" and dirFunc.getFunctionByName(currentFunc)['name'] != dirFunc.getMainName() else False
                ip = currentQuad[3] - 2
                #localMemory.insertNewMemState()
            if (currentQuad[0] == 'RETURN'):
                if (needReturn):
                    lastIp = checkpoints.top()
                    checkpoints.pop()
                    ip = lastIp - 2
                    localMemory.popStack()
                else:
                    Error("Runtime Error: The function", currentFunc, "cant have a return")

            if (currentQuad[0] == 'ENDFUNC'):
                if (needReturn):
                    Error("Runtime Error: The function", currentFunc, "need to be exited by a return statement")
                if (checkpoints.size() > 0):
                    lastIp = checkpoints.top()
                    checkpoints.pop()
                    ip = lastIp - 2
                    localMemory.popStack()
            if (currentQuad[0] == 'VERIFY'):
                val = getFromMemory(currentQuad[1])
                if (val < currentQuad[2] or val > currentQuad[3]):
                    Error("Execution Error: out of bounds")
            if (currentQuad[0] == 'FIND'):
                valToFind = getTransformmedAddress(currentQuad[1])
                startAtAddress = currentQuad[3]
                arrayIndexes = []
                flag = False
                for i in range(currentQuad[2]):
                    try:
                        address = startAtAddress + i
                        if (getTransformmedAddress(address) == valToFind):
                            flag = True
                            print("Value found")
                    except:
                        pass
                if (not flag):
                    print("Value not in array")
            if (currentQuad[0] == 'AVG'):
                startAtAddress = currentQuad[3]
                arrayIndexes = []
                for i in range(currentQuad[2]):
                    try:
                        address = startAtAddress + i
                        val = getTransformmedAddress(address)
                        arrayIndexes.append(val)
                    except:
                        pass
                print("The average is:", statistics.mean(arrayIndexes))
            if (currentQuad[0] == 'MODE'):
                startAtAddress = currentQuad[3]
                arrayIndexes = []
                for i in range(currentQuad[2]):
                    try:
                        address = startAtAddress + i
                        val = getTransformmedAddress(address) 
                        arrayIndexes.append(val)
                    except:
                        pass
                print("The mode is:", statistics.mode(arrayIndexes))
            if (currentQuad[0] == 'PLOT'):
                startAtAddress = currentQuad[3]
                arrayIndexes = []
                for i in range(currentQuad[2]):
                    try:
                        address = startAtAddress + i
                        val = getTransformmedAddress(address) 
                        arrayIndexes.append(val)
                    except:
                        pass
                plt.plot(arrayIndexes)
                plt.show()
            if (currentQuad[0] == 'SORT'):
                startAtAddress = currentQuad[3]
                arrayIndexes = []
                dispIndexes = []
                cont = 0
                for i in range(currentQuad[2]):
                    try:
                        address = startAtAddress + i
                        val = getTransformmedAddress(address) 
                        dispIndexes.append(1)
                        arrayIndexes.append(val)
                    except:
                        dispIndexes.append(-1)
                arrayIndexes.sort()
                for i in range(currentQuad[2]):
                    address = startAtAddress + i
                    if (dispIndexes[i] != -1):
                        insertInMemory(address,arrayIndexes[i])
                        cont += 1
            #if (currentQuad[0] == 'SUMARRAY'):
            #    arrayAddress1 = currentQuad[1]
            #    arrayAddress2 = currentQuad[2]
            #    arrayIndexes1 = []
            #    arrayIndexes2 = []
            #    dispIndexes1 = []
            #    dispIndexes2 = []
            #    cont = 0
            #    var1 = findVariableByAdrresInDir(arrayAddress1, currentFunc)
            #    var2 = findVariableByAdrresInDir(arrayAddress2, currentFunc)
            #    print("DATA", var1, var2)
            #    def getArrayindexes(startAtAddress, size):
            #        dispIndexes = []
            #        arrayIndexes = []
            #        for i in range(size):
            #            try:
            #                address = startAtAddress + i
            #                val = getTransformmedAddress(address) 
            #                dispIndexes.append(1)
            #                arrayIndexes.append(val)
            #            except:
            #                dispIndexes.append(-1)
            #        return dispIndexes, arrayIndexes
            #    dispIndexes1, arrayIndexes1 = getArrayindexes(arrayAddress1, var1["limSup"] - var2["limInf"] + 1)
            #    print(arrayAddress1)
                
                        
            ip += 1
        #print("Global Memory")
        #globalMemory.printMemory()
        #print("Local Memory")
        #localMemory.printMemory()
        #print("Temporal Global Memory")
        #tempGlobalMemory.printMemory()
        #print("Temporal Local Memory")
        #tempLocalMemory.printMemory()

                


