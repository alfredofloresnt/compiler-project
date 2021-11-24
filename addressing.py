from errorHandler import Error

# Address definition
currentIntGlobalAddress = 1000
currentFloatGlobalAddress = 2000
currentCharGlobalAddress = 3000

currentIntLocalAddress = 4000
currentFloatLocalAddress = 5000
currentCharLocalAddress = 6000

currentIntTemporalGlobalAddress = 7000
currentFloatTemporalGlobalAddress = 7500
currentCharTemporalGlobalAddress = 8000
currentIntTemporalLocalAddress = 8500
currentFloatTemporalLocalAddress = 9000
currentCharTemporalLocalAddress = 9500

currentIntConstAddress = 10000
currentFloatConstAddress = 11000
currentCharConstAddress = 12000

def handleAddressing(typeVar, category, add = 1):
    global currentIntGlobalAddress, currentFloatGlobalAddress, currentCharGlobalAddress, currentIntLocalAddress, currentFloatLocalAddress, currentCharLocalAddress, currentIntTemporalAddress, currentFloatTemporalAddress, currentCharTemporalAddress, currentIntConstAddress, currentFloatConstAddress, currentCharConstAddress, currentIntTemporalGlobalAddress, currentFloatTemporalGlobalAddress, currentCharTemporalGlobalAddress, currentIntTemporalLocalAddress, currentFloatTemporalLocalAddress, currentCharTemporalLocalAddress
    if (typeVar == "int" and category == "global" ):
        if (currentIntGlobalAddress >= 1000 and currentIntGlobalAddress <= 1999):
            aux = currentIntGlobalAddress
            currentIntGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "float" and category == "global" ):
        if (currentFloatGlobalAddress >= 2000 and currentFloatGlobalAddress <= 2999):
            aux = currentFloatGlobalAddress
            currentFloatGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "char" and category == "global" ):
        if (currentCharGlobalAddress >= 3000 and currentCharGlobalAddress <= 3999):
            aux = currentCharGlobalAddress
            currentCharGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "int" and category == "local" ):
        if (currentIntLocalAddress >= 4000 and currentIntLocalAddress <= 4999):
            aux = currentIntLocalAddress
            currentIntLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "float" and category == "local" ):
        if (currentFloatLocalAddress >= 5000 and currentFloatLocalAddress <= 5999):
            aux = currentFloatLocalAddress
            currentFloatLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "char" and category == "local" ):
        if (currentCharLocalAddress >= 6000 and currentCharLocalAddress <= 6999):
            aux = currentCharLocalAddress
            currentCharLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "int" and category == "temporalGlobal" ):
        if (currentIntTemporalGlobalAddress >= 7000 and currentIntTemporalGlobalAddress <= 7499):
            aux = currentIntTemporalGlobalAddress
            currentIntTemporalGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "float" and category == "temporalGlobal" ):
        if (currentFloatTemporalGlobalAddress >= 7500 and currentFloatTemporalGlobalAddress <= 7999):
            aux = currentFloatTemporalGlobalAddress
            currentFloatTemporalGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "char" and category == "temporalGlobal" ):
        if (currentCharTemporalGlobalAddress >= 8000 and currentCharTemporalGlobalAddress <= 8499):
            aux = currentCharTemporalGlobalAddress
            currentCharTemporalGlobalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "int" and category == "temporalLocal" ):
        if (currentIntTemporalLocalAddress >= 8500 and currentIntTemporalLocalAddress <= 8999):
            aux = currentIntTemporalLocalAddress
            currentIntTemporalLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "float" and category == "temporalLocal" ):
        if (currentFloatTemporalLocalAddress >= 9000 and currentFloatTemporalLocalAddress <= 9499):
            aux = currentFloatTemporalLocalAddress
            currentFloatTemporalLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "char" and category == "temporalLocal" ):
        if (currentCharTemporalLocalAddress >= 9500 and currentCharTemporalLocalAddress <= 9999):
            aux = currentCharTemporalLocalAddress
            currentCharTemporalLocalAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "int" and category == "constant" ):
        if (currentIntConstAddress >= 10000 and currentIntConstAddress <= 10999):
            aux = currentIntConstAddress
            currentIntConstAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "float" and category == "constant" ):
        if (currentFloatConstAddress >= 11000 and currentFloatConstAddress <= 11999):
            aux = currentFloatConstAddress
            currentFloatConstAddress += add
            return aux
        else:
            Error("AddressingOverflow")
    if (typeVar == "char" and category == "constant" ):
        if (currentCharConstAddress >= 12000 and currentCharConstAddress <= 12999):
            aux = currentCharConstAddress
            currentCharConstAddress += add
            return aux
        else:
            Error("AddressingOverflow")