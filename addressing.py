currentIntGlobalAddress = 1000
currentFloatGlobalAddress = 2000
currentCharGlobalAddress = 300

currentIntLocalAddress = 4000
currentFloatLocalAddress = 5000
currentCharLocalAddress = 600

currentIntTemporalAddress = 7000
currentFloatTemporalAddress = 8000
currentCharTemporalAddress = 900

currentIntConstAddress = 10000
currentFloatConstAddress = 11000
currentCharConstAddress = 12000

def handleAddressing(typeVar, category):
    global currentIntGlobalAddress, currentFloatGlobalAddress, currentCharGlobalAddress, currentIntLocalAddress, currentFloatLocalAddress, currentCharLocalAddress, currentIntTemporalAddress, currentFloatTemporalAddress, currentCharTemporalAddress, currentIntConstAddress, currentFloatConstAddress, currentCharConstAddress
    if (typeVar == "int" and category == "global" ):
        aux = currentIntGlobalAddress
        currentIntGlobalAddress += 1
        return aux
    if (typeVar == "float" and category == "global" ):
        aux = currentFloatGlobalAddress
        currentFloatGlobalAddress += 1
        return aux
    if (typeVar == "char" and category == "global" ):
        aux = currentCharGlobalAddress
        currentCharGlobalAddress += 1
        return aux
    if (typeVar == "int" and category == "local" ):
        aux = currentIntLocalAddress
        currentIntLocalAddress += 1
        return aux
    if (typeVar == "float" and category == "local" ):
        aux = currentFloatLocalAddress
        currentFloatLocalAddress += 1
        return aux
    if (typeVar == "char" and category == "local" ):
        aux = currentCharLocalAddress
        currentCharLocalAddress += 1
        return aux
    if (typeVar == "int" and category == "temporal" ):
        aux = currentIntTemporalAddress
        currentIntTemporalAddress += 1
        return aux
    if (typeVar == "float" and category == "temporal" ):
        aux = currentFloatTemporalAddress
        currentFloatTemporalAddress += 1
        return aux
    if (typeVar == "char" and category == "temporal" ):
        aux = currentCharTemporalAddress
        currentCharTemporalAddress += 1
        return aux
    if (typeVar == "int" and category == "constant" ):
        aux = currentIntConstAddress
        currentIntConstAddress += 1
        return aux
    if (typeVar == "float" and category == "constant" ):
        aux = currentFloatConstAddress
        currentFloatConstAddress += 1
        return aux
    if (typeVar == "char" and category == "constant" ):
        aux = currentCharConstAddress
        currentCharConstAddress += 1
        return aux