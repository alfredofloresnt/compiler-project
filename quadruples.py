# Data strucutres definition
class Stack:
    def __init__(self):
        self.items = []
    def empty(self):
        return self.items == []
    def push(self, item):
        return self.items.append(item)
    def pop(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    def top(self):
        return self.items[len(self.items)-1]
    def printStack(self):
        print(self.items)

class Queue:
    def __init__(self):
        self.items = []
    def empty(self):
        return self.items == []
    def insert(self, item):
        self.items.append(item)
    def remove(self):
        self.items = self.items[1:]
    def front(self):
        return self.items[0]
    def back(self):
        return self.items[len(self.items)-1]
    def printQueue(self):
        print(self.items)

# Quadruples definition
class Quadruples:
    def __init__(self):
        self.operandsStack = Stack()
        self.operationsStack = Stack()
        self.typesStack = Stack()
        self.quad = Stack()
    def getOperandsStack(self):
        return self.operandsStack
    def getOperationsStack(self):
        return self.operationsStack
    def getTypeStack(self):
        return self.typesStack
    def generateQuad(self, operator, leftOperand, rightOperand, result):
        self.quad.push([operator, leftOperand, rightOperand, result])
    def printStacks(self):
        print("operandsStack")
        self.operandsStack.printStack()
        print("operationsStack")
        self.operationsStack.printStack()
        print("typesStack")
        self.typesStack.printStack()
    

    



