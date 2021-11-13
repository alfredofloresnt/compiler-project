import pprint

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



class VirtualMachine():
    def beginMachine(self, quadruples, dirFunc, constantsTable):
        def insertInMemory(address, value):
            if (address >= 1000 and address <= 3999):
                globalMemory.insert(address, value)
            elif (address >= 4000 and address <= 6999):
                localMemory.insert(address, value)
            elif (address >= 7000 and address <= 9999):
                tempMemory.insert(address, value)
            elif (address >= 10000 and address <= 12999):
                constantsMemory.insert(address, value)
        def getFromMemory(address):
            if (address >= 1000 and address <= 3999):
                return globalMemory.get(address)
            elif (address >= 4000 and address <= 6999):
                return localMemory.get(address)
            elif (address >= 7000 and address <= 9999):
                return tempMemory.get(address)
            elif (address >= 10000 and address <= 12999):
                return constantsMemory.get(address)
        #def createConstantMemory():
            # Change keys to address to get quick access
            
            
            
        globalMemory = Memory()
        localMemory = Memory()
        tempMemory = Memory()
        constantsMemory = Memory()
        ip = 0
        currentQuad = quadruples.get(ip)
        currentFunc = None
        #print(quadruples, dirFunc, constantsTable)
        #dirFunc.printDirFunc()
        #print(dirFunc.getMainName())
        # Change keys to address to get quick access
        for key, obj in constantsTable.items():
            constantsMemory.insert(obj['address'], obj['name'])
        while(currentQuad[0] != 'END'):
            currentQuad = quadruples.get(ip)
            print("currentQuad", currentQuad)
            # Big switch case
            if (currentQuad[0] == '='):
                print("Assignation")
                if (currentFunc == None):
                    currentFunc = dirFunc.getMainName()
                newVal = getFromMemory(currentQuad[1])
                resDir = currentQuad[3]
                insertInMemory(resDir, newVal)
            if (currentQuad[0] == '+'):
                valLeft = getFromMemory(currentQuad[1])
                valRight = getFromMemory(currentQuad[2])
                addressTemp = currentQuad[3]
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
            ip += 1
        print("Global Memory")
        globalMemory.printMemory()
        print("Local Memory")
        localMemory.printMemory()
        print("Temporal Memory")
        tempMemory.printMemory()

                


