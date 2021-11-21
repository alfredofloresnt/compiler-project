import pprint
import quadruples as qp

class Memory():
    def __init__(self):
        self.data = {}
    def insert(self, address, value):
        self.data[address] = value
    def get(self, address):
        return self.data[address]
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def printMemory(self):
        pprint.pprint(self.data)

class StackSegment():
    def __init__(self):
        self.data = [{}]
    def insertNewMemState(self):
        self.data.append({})
    def insertTop(self, address, val):
        self.data[len(self.data)-1][address] = val
    def get(self, address):
        return self.data[address]
    def getPreviousState(self, address):
        if (address in self.data[len(self.data)-2]):
            return self.data[len(self.data)-2][address]
        else:
            return None
    def getTop(self, address):
        if (address in self.data[len(self.data)-1]):
            return self.data[len(self.data)-1][address]
        else:
            return None
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def getDataPrev(self):
        return self.data[len(self.data)-2]
    def popStack(self):
        self.data.pop()
    def printMemory(self):
        for x in self.data:
            pprint.pprint(x)



class VirtualMachine():
    def beginMachine(self, quadruples, dirFunc, constantsTable):
        def insertInMemory(address, value):
            if (address >= 1000 and address <= 3999):
                globalMemory.insert(address, value)
            elif (address >= 4000 and address <= 6999):
                localMemory.insertTop(address, value)
            elif (address >= 7000 and address <= 8499):
                tempGlobalMemory.insert(address, value)
            elif (address >= 8500 and address <= 9999):
                tempLocalMemory.insert(address, value)
            elif (address >= 10000 and address <= 12999):
                constantsMemory.insert(address, value)
        def getFromMemory(address):
            if (address >= 1000 and address <= 3999):
                return globalMemory.get(address)
            elif (address >= 4000 and address <= 6999):
                if localMemory.getTop(address):
                    return localMemory.getTop(address)
                else:
                    return localMemory.getPreviousState(address)
            elif (address >= 7000 and address <= 8499):
                return tempGlobalMemory.get(address)
            elif (address >= 8500 and address <= 9999):
                return tempLocalMemory.get(address)
            elif (address >= 10000 and address <= 12999):
                return constantsMemory.get(address)
        def getLocalOrGlobal(address):
            if (localMemory.getPreviousState(address)):
                return localMemory.getPreviousState(address)
            elif (globalMemory.get(address)):
                return globalMemory.get(address)
        #def createConstantMemory():
            # Change keys to address to get quick access
            
            
   
        globalMemory = Memory()
        localMemory = StackSegment()
        checkpoints = qp.Stack()
        tempLocalMemory = Memory()
        tempGlobalMemory = Memory()
        constantsMemory = Memory()
        ip = 0
        paramsStore = []
        currentQuad = quadruples.get(ip)
        currentFunc = dirFunc.getMainName()
        #print(quadruples, dirFunc, constantsTable)
        #dirFunc.printDirFunc()
        #print(dirFunc.getMainName())
        # Change keys to address to get quick access
        for key, obj in constantsTable.items():
            constantsMemory.insert(obj['address'], obj['name'])
        while(currentQuad[0] != 'END'):
            currentQuad = quadruples.get(ip)
            #print("currentQuad", currentQuad)
            # Big switch case
            if (currentQuad[0] == '='):     
                newVal = getFromMemory(currentQuad[1])
                resDir = currentQuad[3]
                insertInMemory(resDir, newVal)
            if (currentQuad[0] == '+'):
                #   tempMemory.printMemory()
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                if (valRight == None): # Check if is an addres or a value from an array operation
                    valRight = currentQuad[2]
                addressTemp = currentQuad[3]
                print("valLeft + valRight", valLeft, valRight)
                insertInMemory(addressTemp, valLeft + valRight)
            if (currentQuad[0] == '-'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft - valRight)
            if (currentQuad[0] == '*'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft * valRight)
            if (currentQuad[0] == '/'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                insertInMemory(addressTemp, valLeft / valRight)
            if (currentQuad[0] == 'GoTo'):
                ip = currentQuad[3] - 2 # -2 Because quads start at index 0 and add one more iteration
            if (currentQuad[0] == 'GoToF'):
                val = getFromMemory(currentQuad[1])
                if (val == 0):
                    ip = currentQuad[3] - 2
            if (currentQuad[0] == '<'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft < valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '>'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft > valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '>='):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft >= valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '<='):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft <= valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '!='):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft != valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '=='):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == valRight):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '&&'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == 1 and valRight == 1):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == '||'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
                if (valLeft == 1 or valRight == 1):
                    insertInMemory(addressTemp, 1)
                else:
                    insertInMemory(addressTemp, 0)
            if (currentQuad[0] == 'PRINT'):
                
                val = getFromMemory(currentQuad[3])
                print(val)
            if (currentQuad[0] == 'READ'):
                varToBeAssigned = currentQuad[1]
                val = input()
                def getType(s):
                    try:
                        int(s)
                        return "int" 
                    except ValueError:
                        try:
                            float(s)
                            return "float"
                        except ValueError:
                            str(s)
                            return "char"
                valType = getType(val)
                if (valType == "char"):
                    val = val[0]
                insertInMemory(varToBeAssigned, val)
            if (currentQuad[0] == 'ERA'):
                #Validate space
                paramsStore = []
                #print("data1", localMemory.getDataPrev())
                
                for key, obj in dirFunc.getFunctionByName(currentQuad[1])['table'].getData().items():
                    paramsStore.append({'name': obj['name'], 'address': obj['address'], 'type': obj['type']})
            if (currentQuad[0] == 'PARAMETER'):
                paramIndex = currentQuad[3]-1
                address = paramsStore[paramIndex]['address']
                val = getFromMemory(currentQuad[1])
                insertInMemory(address, val)
            if (currentQuad[0] == 'GOSUB'):
                saveQuad = ip + 2
                checkpoints.push(saveQuad)
                currentFunc = currentQuad[1]
                #print("RETURNDATA", dirFunc.getFunctionByName(currentFunc)['type'], dirFunc.getFunctionByName(currentFunc)['name'],  dirFunc.getMainName())
                needReturn = True if dirFunc.getFunctionByName(currentFunc)['type'] != "void" and dirFunc.getFunctionByName(currentFunc)['name'] != dirFunc.getMainName() else False
                ip = currentQuad[3] - 2
                localMemory.insertNewMemState()
            if (currentQuad[0] == 'RETURN'):
                if (needReturn):
                    lastIp = checkpoints.top()
                    checkpoints.pop()
                    ip = lastIp - 2
                    localMemory.popStack()
                else:
                    print("Runtime Error: The function", currentFunc, "cant have a return")

            if (currentQuad[0] == 'ENDFUNC'):
                if (needReturn):
                    print("Runtime error: The function", currentFunc, "need to be exited by a return statement")
                if (checkpoints.size() > 0):
                    lastIp = checkpoints.top()
                    checkpoints.pop()
                    ip = lastIp - 2
                    localMemory.popStack()
            if (currentQuad[0] == 'VERIFY'):
                val = getFromMemory(currentQuad[1])
                if (val < currentQuad[2] or val > currentQuad[3]):
                    print("Execution Error: out of bounds")
                
            ip += 1
        print("Global Memory")
        globalMemory.printMemory()
        print("Local Memory")
        localMemory.printMemory()
        print("Temporal Global Memory")
        tempGlobalMemory.printMemory()
        print("Temporal Local Memory")
        tempLocalMemory.printMemory()

                


