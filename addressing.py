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
        print("ADDRESSING", currentIntGlobalAddress, typeVar, category)
        aux = currentIntGlobalAddress
        currentIntGlobalAddress += add
        return aux
    if (typeVar == "float" and category == "global" ):
        aux = currentFloatGlobalAddress
        currentFloatGlobalAddress += add
        return aux
    if (typeVar == "char" and category == "global" ):
        aux = currentCharGlobalAddress
        currentCharGlobalAddress += add
        return aux
    if (typeVar == "int" and category == "local" ):
        aux = currentIntLocalAddress
        currentIntLocalAddress += add
        return aux
    if (typeVar == "float" and category == "local" ):
        aux = currentFloatLocalAddress
        currentFloatLocalAddress += add
        return aux
    if (typeVar == "char" and category == "local" ):
        aux = currentCharLocalAddress
        currentCharLocalAddress += add
        return aux
    if (typeVar == "int" and category == "temporalGlobal" ):
        aux = currentIntTemporalGlobalAddress
        currentIntTemporalGlobalAddress += add
        return aux
    if (typeVar == "float" and category == "temporalGlobal" ):
        aux = currentFloatTemporalGlobalAddress
        currentFloatTemporalGlobalAddress += add
        return aux
    if (typeVar == "char" and category == "temporalGlobal" ):
        aux = currentCharTemporalGlobalAddress
        currentCharTemporalGlobalAddress += add
        return aux
    if (typeVar == "int" and category == "temporalLocal" ):
        aux = currentIntTemporalLocalAddress
        currentIntTemporalLocalAddress += add
        return aux
    if (typeVar == "float" and category == "temporalLocal" ):
        aux = currentFloatTemporalLocalAddress
        currentFloatTemporalLocalAddress += add
        return aux
    if (typeVar == "char" and category == "temporalLocal" ):
        aux = currentCharTemporalLocalAddress
        currentCharTemporalLocalAddress += add
        return aux
    if (typeVar == "int" and category == "constant" ):
        aux = currentIntConstAddress
        currentIntConstAddress += add
        return aux
    if (typeVar == "float" and category == "constant" ):
        aux = currentFloatConstAddress
        currentFloatConstAddress += add
        return aux
    if (typeVar == "char" and category == "constant" ):
        aux = currentCharConstAddress
        currentCharConstAddress += add
        return aux