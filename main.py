
import ply.lex as lex
import ply.yacc as yacc
import varTables as vt
import quadruples as qp
import semanticCube as sc
import constantTable as ct
import addressing
import virtualMachine as vm
from errorHandler import Error
import random
import traceback
import pickle
# Lexer

# Definicion de tokens
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'program' : 'PROGRAM',
    'print' : 'PRINT',
    'vars' : 'VARS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char': 'CHAR',
    'main': 'MAIN',
    'for': 'FOR',
    'while': 'WHILE',
    'to': 'TO',
    'void': 'VOID',
    'read': 'READ',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'avg': 'AVG',
    'reverse': 'REVERSE',
    'find': 'FIND',
    'mode': 'MODE',
}

tokens = ['LETTER', 
          'DIGIT', 
          'DIGITS', 
          'ID', 
          'cteint', 
          'ctefloat',
          'ctechar', 
          'ctestring', 
          'RELOP',
          'RELOP2',
          'EQUAL',
          'LPAREN',
          'RPAREN', 
          'LBRACKET', 
          'RBRACKET',
          'LSQUAREBRACKET', 
          'RSQUAREBRACKET',
          'TWOPOINTS',
          'OPERATORTYPE1',
          'OPERATORTYPE2',
          'LOGICOPERATOR',
          'SEMICOLON',
          'COMMA',
          'THREEDOTS'] + list(reserved.values())

# Definicion de Expresiones Regulares
t_PROGRAM = r'program'
t_IF = r'if'
t_ELSE = r'else'
#t_LETTER = r'[A-Za-z]'
#t_DIGIT = r'[0-9]'
#t_DIGITS = r'[0-9]+'
t_INT = r'int'
t_FLOAT = r'float'
t_PRINT = r'print'
t_ctestring = r'\".*\"'
t_RELOP = r'(?:<=?|>=?|==|!=)'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSQUAREBRACKET = r'\['
t_RSQUAREBRACKET = r'\]'
t_TWOPOINTS = r':'
t_OPERATORTYPE1 = r'\+|\-'
t_OPERATORTYPE2 = r'(\*|\/)'
t_LOGICOPERATOR = r'(\&\&|\|\|)'
t_SEMICOLON = r';'
t_COMMA = r','
t_THREEDOTS = r'(\.\.\.)'
t_ignore = ' '

def t_ctefloat(t):
    r'([0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_cteint(t):
    r'[0-9][0-9]*'
    t.value = int(t.value)
    return t

def t_ctechar(t):
    r'\'[a-zA-Z]\''
    t.value = t.value
    return t

def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9]+)*'
    t.type = reserved.get(t.value,'ID')    # Validar que no exista palabra reservada
    return t

def t_NEWLINE(t):
    r'\n'
    pass


def t_error(t):
    print("Error: Character not defined: ", t.value[0])
    t.lexer.skip(1)


#Build lexer
lexer = lex.lex()
print("Lexer has been genereated!")
    

##################
# Global variables
##################

dirFunc = None
rowVarsAux = {}
currentFunc = None
currentFuncAux = None
currentType = None
currentVarTable = None
currentParamTable = None
currentArrayNodeAux = None
globalFunctionName = None
paramCounter = 0
funcCalled = None
funcCalledStack = []
quadruples = qp.Quadruples()
quadruples.generateQuad('GoTo', 'empty', 'empty', None)
constantsTable = ct.ConstantsTable()
VControl = None
expType = None
DIM = 1
R = 1
offset = 0
size = 0
K = 0
# YACC
def p_PROGRAM(p):
    '''program : PROGRAM ID np2CreateMainVarsTable SEMICOLON program2
               | PROGRAM ID np2CreateMainVarsTable SEMICOLON program3
               | PROGRAM ID np2CreateMainVarsTable SEMICOLON program4'''

def p_PROGRAM2(p):
    '''program2 : decVars program3
                | decVars program4'''

def p_PROGRAM3(p):
    '''program3 : functions program4'''
    
def p_PROGRAM4(p):
    '''program4 : MAIN npGoToMain npChangeCurrentFunctionToMain LPAREN RPAREN npCountQuadruples block npEndMain'''

def p_DEC_VARS(p):
    '''decVars : VARS np3CreateVarsTable decVars2
                | empty'''   

def p_DEC_VARS2(p):
    '''decVars2 : type TWOPOINTS decVars3'''
    
def p_DEC_VARS3(p):
    '''decVars3 : ID np4AddCurrentTable decVars4
                | decVarsArray
                | ID np4AddCurrentTable decVars6'''

def p_DEC_VARS4(p):
    '''decVars4 : COMMA decVars3'''

def p_DEC_VARS5(p):
    '''decVarsArray : ID np4AddCurrentTable npSetAsArray LSQUAREBRACKET cteint THREEDOTS cteint npSetArrayDim RSQUAREBRACKET npArrayOffset decVars4
                | ID np4AddCurrentTable npSetAsArray LSQUAREBRACKET cteint THREEDOTS cteint npSetArrayDim RSQUAREBRACKET  npArrayOffset decVars6'''

def p_DEC_VARS6(p):
    '''decVars6 : SEMICOLON decVars2
                | SEMICOLON'''
    
    
def p_FUNCTIONS(p):
    '''functions : function functions
                | function'''
    
def p_FUNCTION(p):
    '''function : FUNCTION type ID np9AddFunction np3CreateVarsTable LPAREN param RPAREN npCountParameters decVars npCountLocalVars npCountQuadruples block np12DeleteCurrentVarsTable npEndProc
                | FUNCTION VOID np8SetCurrentTypeVoid ID np9AddFunction np3CreateVarsTable LPAREN param RPAREN npCountParameters decVars npCountLocalVars npCountQuadruples block np12DeleteCurrentVarsTable npEndProc'''

def p_PARAM(p):
    '''param : type TWOPOINTS ID npAddParametersCurrentTable empty
             | type TWOPOINTS ID npAddParametersCurrentTable COMMA param
             | empty'''


def p_TYPE(p):
    '''type : INT np5SetCurrentType
            | FLOAT np5SetCurrentType
            | CHAR np5SetCurrentType'''

def p_BLOCK(p):
    '''block : LBRACKET block2'''
    
def p_BLOCK2(p):
    '''block2 : block3
               | block4'''

def p_BLOCK3(p):
    '''block3 : statement block2'''

def p_BLOCK4(p):
    '''block4 : RBRACKET'''

def p_STATEMENT(p):
    '''statement : assignation
                | condition
                | print
                | whileLoop
                | readInput
                | returnFunc
                | functionCall
                | forLoop
                '''

def p_ASSIGNATION(p):
    '''assignation : variable EQUAL qnp2_push_operations expression assigmentnp SEMICOLON'''

def p_VARIABLE(p):
    '''variable : ID qnp1_push variable2
                | ID qnp1_push'''

def p_VARIABLE2(p):
    '''variable2 : LSQUAREBRACKET npArrayAccessPushDim variable3 npArrayAccessVerifyLimits RSQUAREBRACKET npArrayAccessGenerateQuad'''

def p_VARIABLE3(p):
    '''variable3 : expression'''
        
def p_PRINT_ON_SCREEN(p):
    '''print : PRINT LPAREN print2'''

def p_PRINT_ON_SCREEN2(p):
    '''print2 : expression npPrint print3  
              | ctestring npPrint print3'''

def p_PRINT_ON_SCREEN3(p):
    '''print3 : COMMA print2
              | RPAREN SEMICOLON'''

def p_WHILE_LOOP(p):
    '''whileLoop : WHILE npWhile1 LPAREN superExpression RPAREN npWhile2 block npWhile3'''

def p_FOR_LOOP(p):
    '''forLoop : FOR LPAREN ID np1For EQUAL exp np2For TO exp np3For RPAREN block np4For'''

def p_RETURN_FUNC(p):
    '''returnFunc : RETURN LPAREN superExpression npReturn RPAREN SEMICOLON'''

def p_READ_INPUT(p):
    '''readInput : READ LPAREN variable npRead RPAREN SEMICOLON'''


def p_SUPER_EXPRESSION(p):
    '''superExpression : expression qnp7_push_logicOperation_apply
                 | expression LOGICOPERATOR qnp2_push_operations expression qnp7_push_logicOperation_apply'''

def p_EXPRESSION(p):
    '''expression : exp qnp6_push_operationtypeRELOP_apply
                 | exp RELOP qnp2_push_operations exp qnp6_push_operationtypeRELOP_apply'''

def p_CONDITION(p):
    '''condition : IF LPAREN superExpression ifnp1 RPAREN block ifnp2End
                 | IF LPAREN superExpression ifnp1 RPAREN block ELSE ifnp3Else block ifnp2End'''
    


def p_FUNCTION_CALL(p):
    '''functionCall : ID npVerifyFunc npCreateEra LPAREN functionCall2 RPAREN npVerifyParamsCoherency
                    | ID npVerifyFunc npCreateEra LPAREN RPAREN npVerifyParamsCoherency'''

def p_FUNCTION_CALL2(p):
    '''functionCall2 : superExpression npVerifyParam 
                     | superExpression npVerifyParam COMMA npMoveNextParam functionCall2'''

def p_EXP(p):
    '''exp : term qnp4_push_operationtype1_apply exp2'''

def p_EXP2(p):
    '''exp2 : OPERATORTYPE1 qnp2_push_operations exp
            | empty'''

def p_TERM(p):
    '''term : factor qnp5_push_operationtype2_apply term2'''

def p_TERM2(p):
    '''term2 : OPERATORTYPE2 qnp2_push_operations term
             | empty'''

def p_FACTOR(p):
    '''factor : LPAREN npPushFakeBottom superExpression RPAREN npPopFakeBottom
              | factor2 varcte
              | ID qnp1_push factor3
              | functionFactor
              | varcte'''

def p_FACTOR2(p):
    '''factor2 : OPERATORTYPE1'''

def p_FACTOR3(p):
    '''factor3 : LSQUAREBRACKET npArrayAccessPushDim expression npArrayAccessVerifyLimits RSQUAREBRACKET npArrayAccessGenerateQuad'''

def p_FUNCTION_FACTOR(p):
    '''functionFactor : ID npFunctionPushFactor npVerifyFuncFactor npCreateEraFactor LPAREN functionCall2Factor RPAREN npVerifyParamsCoherencyFactor'''

def p_FUNCTION_CALL2_FACTOR(p):
    '''functionCall2Factor : superExpression npVerifyParamFactor 
                     | superExpression npVerifyParamFactor COMMA npMoveNextParam functionCall2Factor '''
#def p_FACTOR4(p):
#    '''factor4 : expression COMMA factor4
#                | expression RPAREN'''

#def p_FACTOR5(p):
#    '''factor5 : expression COMMA factor5
#                | expression npArrayAccessVerifyLimits RSQUAREBRACKET npArrayAccessGenerateQuad'''

def p_VARCTE(p):
    '''varcte : ID qnp1_push
              | cteint npAddCTEINT
              | ctefloat npAddCTEFLOAT
              | ctechar npAddCTECHAR'''

def p_EMPTY(p):
    '''empty :'''
    pass

# Neuralgic points

def p_TEST(p):
    '''np0Test : empty'''
    print("ENTRA TEST")

def p_GOTO_MAIN(p):
    '''npGoToMain : empty'''
    cont = quadruples.getQuad().size() + 1
    quadruples.fillQuad(1, cont)




def p_NP2_CREATE_MAIN_VARS_TABLE(p):
    '''np2CreateMainVarsTable : empty'''
    global dirFunc
    global currentFunc
    global globalFunctionName
    dirFunc = vt.DirFunc()
    dirFunc.insert({"name": p[-1], "type": "global", "table": None})
    globalFunctionName = p[-1]
    currentFunc = p[-1]

def p_CHANGE_CURRENT_FUNCTION_TO_MAIN(p):
    '''npChangeCurrentFunctionToMain : empty'''
    global currentFunc
    global currentVarTable
    global currentParamTable
    #print("globalFunctionName", currentFunc, globalFunctionName)
    currentFunc = globalFunctionName
    currentVarTable = dirFunc.getFunctionByName(globalFunctionName)["table"]
    currentParamTable = dirFunc.getFunctionByName(globalFunctionName)["parameterTable"]

def p_NP3_CREATE_VARS_TABLE(p):
    '''np3CreateVarsTable : empty'''
    global dirFunc
    global currentVarTable
    global currentParamTable
    row = dirFunc.getFunctionByName(currentFunc)
    if (row["table"] == None):
        currentParamTable = vt.Params() 
        currentVarTable = vt.Vars()
        dirFunc.addVarsTable(currentFunc, currentVarTable)
        dirFunc.addParametersTable(currentFunc, currentParamTable)
        

def p_NP4_ADD_CURRENT_TABLE(p):
    '''np4AddCurrentTable : empty'''
    global currentVarTable
    global currentParamTable
    global currentType
    # Check if id-name in current VarsTable
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        Error("Semantic Error: Multiple variable declaration of " + p[-1])
    else:
        if (currentFunc == globalFunctionName):
            currentVarTable.insert({"name": p[-1], "type": currentType, "address": addressing.handleAddressing(currentType, "global")})
        else:
            currentVarTable.insert({"name": p[-1], "type": currentType, "address": addressing.handleAddressing(currentType, "local")})

def p_ADD_PARAMETERS_CURRENT_TABLE(p):
    '''npAddParametersCurrentTable : empty '''
    global currentVarTable
    global currentParamTable
    global currentType
    # Check if id-name in current VarsTable
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        Error("Semantic Error: Multiple variable declaration of " + p[-1])
    else:
        currentVarTable.insert({"name": p[-1], "type": currentType, "address": addressing.handleAddressing(currentType, "local")})
        currentParamTable.insert(currentType)
        

def p_COUNT_PARAMETERS(p):
    '''npCountParameters : empty'''
    totParams = currentParamTable.getSize()
    dirFunc.setTotParameters(currentFunc, totParams)

def p_COUNT_LOCAL_VARS(p):
    '''npCountLocalVars : empty'''
    totLocalVars = currentVarTable.getSize()
    dirFunc.setTotLocalVars(currentFunc, totLocalVars)

def p_COUNT_QUADRUPLES(p):
    '''npCountQuadruples : empty'''
    cont = quadruples.getQuad().size() + 1
    dirFunc.setCountQuadruples(currentFunc, cont)

def p_END_PROC(p):
    '''npEndProc : empty'''
    # To-do: Clear current varTable
    quadruples.generateQuad('ENDFUNC', 'empty', 'empty', 'empty')

def p_VERIFY_FUNCTION(p):
    '''npVerifyFunc : empty'''
    global funcCalledStack, funcCalled
    if (dirFunc.getFunctionByName(p[-1]) == None):
        Error("Semantic Error: Function not declared")
    else:
        funcCalledStack.append(p[-1])
        funcCalled = funcCalledStack[-1]

def p_CREATE_ERA(p):
    '''npCreateEra : empty'''
    global paramCounter
    global currentFuncAux
    global currentFunc
    global currentParamTable
    quadruples.generateQuad("ERA", funcCalled, 'empty', 'empty')
    paramCounter = 1
    currentFuncAux = currentFunc
    
    currentParamTable = dirFunc.getFunctionByName(funcCalled)["parameterTable"]

def p_VERIFY_PARAM(p):
    '''npVerifyParam : empty'''
    global paramCounter
    argument = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    argumentType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    paramTypeInTable = currentParamTable.getParamByIndex(paramCounter - 1)
    if (argumentType == paramTypeInTable):
        quadruples.generateQuad("PARAMETER", argument, "empty", paramCounter)
    else:
        Error("Semantic Error: Wrong funtion signature", argumentType, "is not", paramTypeInTable)

def p_MOVE_NEXT_PARAM(p):
    '''npMoveNextParam : empty'''
    global paramCounter
    paramCounter += 1

def p_VERIFY_PARAMS_COHERENCY(p):
    '''npVerifyParamsCoherency : empty'''
    global funcCalledStack, funcCalled
    paramTable = dirFunc.getFunctionByName(funcCalled)['parameterTable']
    if (paramTable.getParamByIndex(paramCounter) != None):
        Error("Semantic Error: Params number does not match", paramCounter, paramTable.getSize())
    else:
        quadruples.generateQuad("GOSUB", funcCalled, 'empty', dirFunc.getStartAtQuad(funcCalled))
        funcCalledType = dirFunc.getFunctionByName(funcCalled)["type"]
        currentFunc = funcCalled
        
        if (funcCalledType != "void"):
            # Not void. Save return value to temp
            funcCalledAddres = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(funcCalled)['address']
            temporalType = "temporalLocal" if currentFuncAux != globalFunctionName else "temporalGlobal"
            quadruples.generateQuad("=", funcCalledAddres, 'empty', addressing.handleAddressing(funcCalledType, temporalType))

    funcCalledStack.pop()
    if (len(funcCalledStack) > 0):
        funcCalled = funcCalledStack[-1]
    else:
        funcCalled = None
    


########################
def p_FUNCTION_PUSH_FACTOR(p):
    '''npFunctionPushFactor : empty'''
    
    funcAddress = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1])['address']
    funcType = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1])['type']
    quadruples.getOperandsStack().push(funcAddress)
    quadruples.getTypeStack().push(funcType)
    #quadruples.getOperationsStack().push("(")
    

def p_VERIFY_FUNCTION_FACTOR(p):
    '''npVerifyFuncFactor : empty'''
    global funcCalledStack, funcCalled
    if (dirFunc.getFunctionByName(p[-2]) == None):
        Error("Semantic Error: Function not declared")
    else:
        funcCalledStack.append(p[-2])
        funcCalled = funcCalledStack[-1]

def p_CREATE_ERA_FACTOR(p):
    '''npCreateEraFactor : empty'''
    global paramCounter
    global currentFuncAux
    global currentFunc
    global currentParamTable
    print("AQUI ENTRA", currentFunc, funcCalled)
    quadruples.generateQuad("ERA", funcCalled, 'empty', 'empty')
    paramCounter = 1
    currentFuncAux = currentFunc
    
    currentParamTable = dirFunc.getFunctionByName(funcCalled)["parameterTable"]

def p_VERIFY_PARAM_FACTOR(p):
    '''npVerifyParamFactor : empty'''
    global paramCounter
    print("==========")
    quadruples.printStacks()
    print("==========")
    argument = quadruples.getOperandsStack().top()
    print("El argumento es ", argument)
    quadruples.getOperandsStack().pop()
    argumentType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    paramTypeInTable = currentParamTable.getParamByIndex(paramCounter - 1)
    if (argumentType == paramTypeInTable):
        quadruples.generateQuad("PARAMETER", argument, "empty", paramCounter)
    else:
        Error("Semantic Error: Wrong funtion signature", argumentType, "is not", paramTypeInTable)


def p_VERIFY_PARAMS_COHERENCY_FACTOR(p):
    '''npVerifyParamsCoherencyFactor : empty'''
    global funcCalledStack, funcCalled
    paramTable = dirFunc.getFunctionByName(funcCalled)['parameterTable']
    if (paramTable.getParamByIndex(paramCounter) != None):
        Error("Semantic Error: Params number does not match", paramCounter, paramTable.getSize())
    else:
        quadruples.generateQuad("GOSUB", funcCalled, 'empty', dirFunc.getStartAtQuad(funcCalled))
        funcCalledType = dirFunc.getFunctionByName(funcCalled)["type"]
        currentFunc = funcCalled
        if (funcCalledType != "void"):
            # Not void. Save return value to temp
            dirFunc.getVarsTableByFunctionName(globalFunctionName).printVars()
            funcCalledAddres = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(funcCalled)['address']
            temporalType = "temporalLocal" if currentFuncAux != globalFunctionName else "temporalGlobal"
            funcTempGlobalAddress = addressing.handleAddressing(funcCalledType, temporalType)
            quadruples.generateQuad("=", funcCalledAddres, 'empty', funcTempGlobalAddress)
            quadruples.getOperandsStack().pop()
            quadruples.getTypeStack().pop()
            quadruples.getOperandsStack().push(funcTempGlobalAddress)
            quadruples.getTypeStack().push(funcCalledType)
    funcCalledStack.pop()
    if (len(funcCalledStack) > 0):
        funcCalled = funcCalledStack[-1]
    else:
        funcCalled = None


#######################

def p_NP5_SET_CURRENT_TYPE(p):
    '''np5SetCurrentType : empty'''
    global currentType
    currentType = p[-1]

def p_NP6_DELETE_DIRFUNC_AND_CURRENT_VARTABLE(p):
    '''np6DeleteDirFuncAndCurrentVarTable : empty'''

def p_NP8_SET_CURRENT_TYPE_VOID(p):
    '''np8SetCurrentTypeVoid : empty'''
    global currentType
    currentType = p[-1]

def p_NP9_ADD_FUNCTION(p):
    '''np9AddFunction : empty'''
    global currentType
    global currentFunc
    # Check if id-name in dirFunc
    row = dirFunc.getFunctionByName(p[-1])
    if (row != None):
        Error("Semantic Error: Multiple function declaration of " + p[-1])
    else:
        dirFunc.insert({"name": p[-1], "type": currentType, "table": None})
        currentFunc = p[-1]

def p_NP12_DELETE_CURRENT_VARS_TABLE(p):
    '''np12DeleteCurrentVarsTable : empty'''
    global currentVarTable
    currentVarTable = None


def p_error(t):
    print("Error (Syntax):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

# Quadruples Neuralgic points 
def p_ADD_CTEINT(p):
    '''npAddCTEINT : empty'''
    quadruples.getTypeStack().push('int')
    if (constantsTable.getConstantByName(p[-1]) == None):
        constantsTable.insert(p[-1], addressing.handleAddressing('int', 'constant'))
    addressINT = constantsTable.getConstantByName(p[-1])['address']
    quadruples.getOperandsStack().push(addressINT)
    #quadruples.getOperandsStack().push(p[-1]) # Add variable name (NOT ADDRESS) in quadruple

def p_ADD_CTEFLOAT(p):
    '''npAddCTEFLOAT : empty'''
    
    quadruples.getTypeStack().push('float')
    if (constantsTable.getConstantByName(p[-1]) == None):
        constantsTable.insert(p[-1], addressing.handleAddressing('float', 'constant'))
    addressFLOAT = constantsTable.getConstantByName(p[-1])['address']
    quadruples.getOperandsStack().push(addressFLOAT)
    #quadruples.getOperandsStack().push(p[-1]) # Add variable name (NOT ADDRESS) in quadruple

def p_ADD_CTECHAR(p):
    '''npAddCTECHAR : empty'''
    quadruples.getTypeStack().push('char')
    if (constantsTable.getConstantByName(p[-1]) == None):
        constantsTable.insert(p[-1], addressing.handleAddressing('char', 'constant'))
    constantsTable.printConstantTable()
    addressCHAR = constantsTable.getConstantByName(p[-1])['address']
    quadruples.getOperandsStack().push(addressCHAR)
    #quadruples.getOperandsStack().push(p[-1]) # Add variable name (NOT ADDRESS) in quadruple

def p_QNP1_PUSH(p):
    '''qnp1_push : empty'''
    addressID = getAddress(p[-1])
    quadruples.getOperandsStack().push(addressID)
    #quadruples.getOperandsStack().push(p[-1]) # Add variable name (NOT ADDRESS) in quadruple
    # Check if variable is declared on local or global functions and add to stacks
    if (currentVarTable.getVariableByName(p[-1]) != None):
        quadruples.getTypeStack().push(currentVarTable.getVariableByName(p[-1])["type"])
    elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1]) != None):
        quadruples.getTypeStack().push(dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1])["type"])
    else:
        print("Semantic Error: Variable not declared", p[-1])

def p_QNP2_PUSH_OPERATIONS(p):
    '''qnp2_push_operations : empty'''
    quadruples.getOperationsStack().push(p[-1])

def p_PUSH_FAKE_BOTTOM(p):
    '''npPushFakeBottom : empty'''
    quadruples.getOperationsStack().push(p[-1])

def p_PUSH_FAKE_POP(p):
    '''npPopFakeBottom : empty'''
    top = quadruples.getOperationsStack().top()
    quadruples.getOperationsStack().pop()

def getAddress(name):
    #constantsTable.printConstantTable()
    if (currentVarTable.getVariableByName(name)):
        address = currentVarTable.getVariableByName(name)['address']
        return address
    elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(name)):
        address = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(name)['address']
        return address
    else:
        Error("Semantic Error: Type mismatch, variable " + str(name) + " does not exist")

def quadruplesProcess():
    #print("ENTER PROCESS")
    rightOperand = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    rightOperandType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    leftOperand = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    leftOperandType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    operation = quadruples.getOperationsStack().top()
    quadruples.getOperationsStack().pop()
    resultType = sc.getType(leftOperandType, rightOperandType, operation)
    if (resultType != None):
        temporalType = "temporalLocal" if currentFunc != globalFunctionName else "temporalGlobal"
        result =  addressing.handleAddressing(resultType, temporalType) #random.randint(0, 999) # This line has to be modified in the future. Addressing needs to be implemented
        ###############
        #rightOperandAddress = getAddress(rightOperand)
        #leftOperandAddress = getAddress(leftOperand)
        ###############
        quadruples.generateQuad(operation, leftOperand, rightOperand, result)
        quadruples.getOperandsStack().push(result)
        quadruples.getTypeStack().push(resultType)
    else:
        print("Semantic Error: Type mismatch")

def p_QNP4_OPERATIONTYPE1_APPLY(p):
    '''qnp4_push_operationtype1_apply : empty'''
    if (quadruples.getOperationsStack().size() > 0):
        #print("CHECK SUM", quadruples.getOperationsStack().top())
        if (quadruples.getOperationsStack().top() == "+" or quadruples.getOperationsStack().top() == "-"):
            quadruplesProcess()
    
def p_QNP5_OPERATIONTYPE2_APPLY(p):
    '''qnp5_push_operationtype2_apply : empty'''
    if (quadruples.getOperationsStack().size() > 0):
        #print("CHECK MULT", quadruples.getOperationsStack().top())
        if (quadruples.getOperationsStack().top() == "*" or quadruples.getOperationsStack().top() == "/"):
            quadruplesProcess()

def p_QNP6_OPERATIONTYPERELOP_APPLY(p):
    '''qnp6_push_operationtypeRELOP_apply : empty'''
    if (quadruples.getOperationsStack().size() > 0):
        #("CHECK RELOP", quadruples.getOperationsStack().top())
        if (quadruples.getOperationsStack().top() == ">" or quadruples.getOperationsStack().top() == "<" or quadruples.getOperationsStack().top() == "!=" or quadruples.getOperationsStack().top() == "==" or quadruples.getOperationsStack().top() == "<=" or quadruples.getOperationsStack().top() == ">="):
            quadruplesProcess()
    
def p_QNP7_LOGICOPERATION_APPLY(p):
    '''qnp7_push_logicOperation_apply : empty'''
    if (quadruples.getOperationsStack().size() > 0):
        if (quadruples.getOperationsStack().top() == "&&" or quadruples.getOperationsStack().top() == "||"):
            quadruplesProcess()



# Neuralgic point for ASSIGMENT statement
def p_ASSIGMENTNP(p):
    '''assigmentnp : empty'''
    resType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    result = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    idType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    id = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    equalSymbol = quadruples.getOperationsStack().top()
    quadruples.getOperationsStack().pop()
    print("ASSIGMENT", idType, resType, equalSymbol)
    resIDType = sc.getType(idType, resType, '=')
    if (equalSymbol == "=" and resIDType == "valid"):
        # Get local or global address
        #if (currentVarTable.getVariableByName(id)):
        #    address = currentVarTable.getVariableByName(id)['address']
        #elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(id)):
        #    address = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(id)['address']
        #else:
        #    print("Semantic Error: Variable not found in local or global scopes")
        #address = getAddress(id)
        #addressResult = getAddress(result)
        quadruples.generateQuad(equalSymbol, result, 'empty', id) #id
        
    else:
        Error("Semantic Error: Type mismatch " + str(resType) + " cannot be " + str(idType))

# Neuralgic point for PRINT statement
def p_print(p):
    '''npPrint : empty'''
    quadruples.getOperationsStack().push('print')
    if (quadruples.getOperandsStack().size() > 0):
        res = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        #address = getAddress(res)
        # Get constant or local or global address
        #if (constantsTable.getConstantByName(res)):
        #    address = constantsTable.getConstantByName(res)['address']
        #if (currentVarTable.getVariableByName(res)):
        #    address = currentVarTable.getVariableByName(res)['address']
        #elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(res)):
        #    address = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(res)['address']
        quadruples.generateQuad('PRINT', 'empty', 'empty', res) #res
        quadruples.getOperationsStack().pop()
        quadruples.getTypeStack().pop()

# Neuralgic point for READ statement
def p_READ(p):
    '''npRead : empty'''
    quadruples.getOperationsStack().push('print')
    if (quadruples.getOperandsStack().size() > 0):
        res = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad('READ', res, 'empty', 'empty') #res
        quadruples.getOperationsStack().pop()
        quadruples.getTypeStack().pop()
        
# Neuralgic point for RETURN statement
def p_RETURN(p):
    '''npReturn : empty'''
    quadruples.getOperationsStack().push('return')
    if (quadruples.getOperandsStack().size() > 0):
        funcType = dirFunc.getFunctionByName(currentFunc)["type"]
        if (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(currentFunc)):
            funcAddress = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(currentFunc)["address"]
        else:
            funcAddress = addressing.handleAddressing(funcType, "global")
        print("funcAddress", funcAddress)
        dirFunc.getVarsTableByFunctionName(globalFunctionName).insert({"name": currentFunc, "type": funcType, "address": funcAddress})
        res = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        resType = quadruples.getTypeStack().top()
        quadruples.getTypeStack().pop()
        quadruples.getOperationsStack().pop()
        typeOper = sc.getType( funcType, resType, "=")
        if (typeOper == "valid"):
            quadruples.generateQuad('=', res, 'empty', funcAddress) #res
            quadruples.generateQuad('RETURN', 'empty', 'empty', res) #res
        else:
            Error("Semantic Error: Type mismatch " + str(resType) + " can not be " + str(funcType))

# Neuralgic point for IF statement
def p_IFNP1(p):
    '''ifnp1 : empty'''
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (expType != 'int'):
        Error("Semantic Error: Type mismatch, not int")
    else:
        result = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad('GoToF', result, 'empty', None)
        cont = quadruples.getQuad().size() + 1
        quadruples.getJumpsStack().push(cont - 1)

def p_IFNP2_END(p):
    '''ifnp2End : empty'''
    end = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    cont = quadruples.getQuad().size() + 1
    quadruples.fillQuad(end, cont)

def p_IFNP3_ELSE(p):
    '''ifnp3Else : empty'''
    quadruples.generateQuad('GoTo', 'empty', 'empty', None)
    false = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    cont = quadruples.getQuad().size() + 1
    quadruples.getJumpsStack().push(cont - 1)
    quadruples.fillQuad(false, cont)

# Neuralgic point for WHILE statement
def p_NP1_WHILE(p):
    '''npWhile1 : empty'''
    cont = quadruples.getQuad().size() + 1
    quadruples.getJumpsStack().push(cont)

def p_NP2_WHILE(p):
    '''npWhile2 : empty'''
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (expType != 'int'):
        Error("Semantic Error: Type mismatch")
    else:
        result = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad('GoToF', result, 'empty', None)
        cont = quadruples.getQuad().size() + 1
        quadruples.getJumpsStack().push(cont - 1)

def p_NP3_WHILE(p):
    '''npWhile3 : empty'''
    end = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    ret = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    quadruples.generateQuad('GoTo', 'empty', 'empty', ret)
    cont = quadruples.getQuad().size() + 1
    quadruples.fillQuad(end, cont)

# Neuralgic points for FOR statement
def p_NP1_FOR(p):
    '''np1For : empty'''
    idType = None
    # Check if variable exist in local function if not checks global
    if (dirFunc.getFunctionByName(currentFunc)["table"].getVariableByName(p[-1])):
        idAddress = dirFunc.getFunctionByName(currentFunc)["table"].getVariableByName(p[-1])['address']
        idType = dirFunc.getFunctionByName(currentFunc)["table"].getVariableByName(p[-1])['type']
    elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1]) != None):
        idAddress = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1])['address']
        idType = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-1])['type']
    if (idType != None):
        if (idType != 'int' and idType != 'float'):
            Error("Semantic Error: Type mismatch, variable " + str(idType) +  ":" + str(p[-1]) + " is not a numeric value")
        else:
            quadruples.getOperandsStack().push(idAddress)
            quadruples.getTypeStack().push(idType)
    else:
        Error("Semantic Error: Type mismatch, variable " + str(p[-1]) + " does not exist")

def p_NP2_FOR(p):
    '''np2For : empty'''
    global VControl
    VControl = None
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (expType != "int" and expType != "float"):
        Error("Semantic Error: Type mismatch, variable " + str(quadruples.getOperandsStack().top()) + " is not a numeric value")
    else:
        exp = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        VControl = quadruples.getOperandsStack().top()
        controlType = quadruples.getTypeStack().top()
        typeRes = sc.getType( controlType, expType, "=")
        if (typeRes != None):
            quadruples.generateQuad("=", exp, "empty", VControl)
        else:
            Error("Semantic Error: Type mismatch")

def p_NP3_FOR(p):
    '''np3For : empty'''
    global VControl
    global expType
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (currentFunc == globalFunctionName):
        VControl = addressing.handleAddressing(expType, "temporalGlobal", 1)
        VFinal = addressing.handleAddressing(expType, "temporalGlobal", 1)
        tx = addressing.handleAddressing(expType, "temporalGlobal", 1)
    else:
        VControl = addressing.handleAddressing(expType, "temporalLocal", 1)
        VFinal = addressing.handleAddressing(expType, "temporalLocal", 1)
        tx = addressing.handleAddressing(expType, "temporalLocal", 1)
    #VControl = "VControl" # Pending variable. Where is going to be stored?
    #VFinal = "VFinal" # Pending variable. Where is going to be stored?
    #tx = "tx" # Pending variable. Where is going to be stored?
    if (expType == "int" or expType == "float"):
        exp = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad("=", exp, "empty", VFinal)
        quadruples.generateQuad("=", VControl, "empty", tx)
        cont = quadruples.getQuad().size() + 1
        quadruples.getJumpsStack().push(cont - 1)
        quadruples.generateQuad("GoToF", tx, "empty", None)
        cont = quadruples.getQuad().size() + 1
        quadruples.getJumpsStack().push(cont - 1)
    else:
        Error("Semantic Error: Type mismatch")

def p_NP4_FOR(p):
    '''np4For : empty'''
    global expType
    global VControl
    if (currentFunc == globalFunctionName):
        ty = addressing.handleAddressing(expType, "temporalGlobal", 1)
    else:
        ty = addressing.handleAddressing(expType, "temporalLocal", 1)

    quadruples.generateQuad("+", VControl, 1, ty)
    quadruples.generateQuad("=", ty, "empty", VControl)
    quadruples.generateQuad("=", ty, "empty", quadruples.getOperandsStack().top()) # Original ID
    fin = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    ret = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    quadruples.generateQuad("GoTo", "empty", "empty", ret)
    cont = quadruples.getQuad().size() + 1
    quadruples.fillQuad(fin, cont)
    quadruples.getOperandsStack().pop() # Remove original ID
    quadruples.getTypeStack().pop()
 
# Neuralig points for ARRAYS
def p_NP_SET_AS_ARRAY(p):
    '''npSetAsArray : empty'''
    global R
    global DIM
    currentVarTable.getVariableByName(p[-2])['isArray'] = True
    R = 1
    DIM = 1

def p_NP_SET_ARRAY_DIM(p):
    '''npSetArrayDim : empty'''
    global currentArrayNodeAux
    global R
    nodeAux = vt.ArrayDimNode()
    nodeAux.setLimInf(p[-3])
    nodeAux.setLimSup(p[-1])
    R = ( p[-1] - p[-3] + 1) * R
    currentArrayNodeAux = nodeAux
    currentVarTable.getVariableByName(p[-7])['dim'] = nodeAux

def p_NP_ARRAY_OFFSET(p):
    '''npArrayOffset : empty'''
    global currentArrayNodeAux
    global offset
    global size
    global R
    global DIM
    global K
    offset = 0
    size = R
    currentArrayNodeAux.setNextNode(None)
    currentArrayNodeAux = currentVarTable.getVariableByName(p[-9])['dim']
    while(True):
        mDim = R / (currentArrayNodeAux.getLimSup() - currentArrayNodeAux.getLimInf() + 1)
        currentArrayNodeAux.setM(mDim)
        R = mDim
        offset = int(offset + currentArrayNodeAux.getLimInf() * mDim)
        if (currentArrayNodeAux.getNextNode() == None):
            break
        else:
            currentArrayNodeAux = currentArrayNodeAux.getNextNode()
    K = -offset
    currentArrayNodeAux.setM(K)
    idType = currentVarTable.getVariableByName(p[-9])['type']
    if (currentFunc == globalFunctionName):
        currentVarTable.getVariableByName(p[-9])['address'] = addressing.handleAddressing(idType, "global", size - 1) - 1
    else:
        currentVarTable.getVariableByName(p[-9])['address'] = addressing.handleAddressing(idType, "local", size - 1) - 1
    #print("test", currentVarTable.getVariableByName(p[-9])['dim'].printNode())

def p_ARRAY_ACCESS_PUSH_DIM(p):
    '''npArrayAccessPushDim : empty'''
    global DIM
    global currentArrayNodeAux
    id = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    idType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (currentVarTable.getVariableByName(p[-3]) and 'dim' in currentVarTable.getVariableByName(p[-3])):
        DIM = 1
        #quadruples.getDimsStack().push(id, DIM)
        currentArrayNodeAux = currentVarTable.getVariableByName(p[-3])['dim']
        quadruples.getOperationsStack().push('(') # Push fake bottom. Dont need it beacause the compiler only handles one dimension
    elif(dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-3]) and 'dim' in dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-3])):
        DIM = 1
        #quadruples.getDimsStack().push(id, DIM)
        currentArrayNodeAux = dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(p[-3])['dim']
        quadruples.getOperationsStack().push('(') # Push fake bottom. Dont need it beacause the compiler only handles one dimension
    else:
        Error("Semantic Error: The variable " + str(p[-3]) + " is not an array")
    
def p_ARRAY_ACCESS_VERIFY_LIMITS(p):
    '''npArrayAccessVerifyLimits : empty '''
    limInf = currentArrayNodeAux.getLimInf()
    limSup = currentArrayNodeAux.getLimSup()
    quadruples.generateQuad('VERIFY',  quadruples.getOperandsStack().top(), limInf, limSup)


def getVariableGlobalorLocal(name):
    if (currentVarTable.getVariableByName(name)):
        return currentVarTable.getVariableByName(name)
    elif (dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(name)):
        return dirFunc.getVarsTableByFunctionName(globalFunctionName).getVariableByName(name)
    else:
        Error("Semantic Error: Variable not found")

def p_ARRAY_ACCESS_GENERATE_QUAD(p):
    '''npArrayAccessGenerateQuad : empty'''
    global constantsTable
    aux1 = quadruples.getOperandsStack().top()
    quadruples.getOperandsStack().pop()
    aux1Type = quadruples.getTypeStack().top()
    temporalType = "temporalLocal" if currentFunc != globalFunctionName else "temporalGlobal"
    tempAddress =  addressing.handleAddressing(aux1Type, temporalType)
    idAddress = getVariableGlobalorLocal(p[-7])['address']
    idType = getVariableGlobalorLocal(p[-7])['type']
    temp2Address =  addressing.handleAddressing(idType, temporalType)
    
    if (constantsTable.getConstantByName(K) == None):
        constAddress = addressing.handleAddressing('int', 'constant')
        constantsTable.insert(K, constAddress)
    else:
        constAddress = constantsTable.getConstantByName(K)["address"]
    quadruples.generateQuad('+', aux1, constAddress, tempAddress)
    quadruples.generateQuad('+', tempAddress, "*" + str(idAddress), temp2Address)
    quadruples.getOperandsStack().push("("+str(temp2Address)+")")
    quadruples.getOperationsStack().pop()

def p_END_MAIN(p):
    '''npEndMain : empty'''
    quadruples.generateQuad("END", 'empty', 'empty', 'empty')

# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")


codeToCompile = open('code3.txt','r')
data = str(codeToCompile.read())
lexer.input(data)
# Debug tokens
while True:
    tok = lexer.token()
    if not tok: 
        break # No more input
    print(tok)
try:
    
    parser.parse(data)
    quadruples.printQuads()
    #quadruples.printStacks()
    #dirFunc.getFunctionByName("test123")['parameterTable'].printParams()
    dirFunc.getFunctionByName("MyRlike")['table'].printVars()
    #dirFunc.getFunctionByName("dos")['table'].printVars()
    #dirFunc.printDirFunc()
    constantsTable.printConstantTable()
    print('Code passed!')
except Exception as e:
    traceback.print_exc()
    print('Error in code!', e)


with open('object.code', 'wb') as handle:
    pickle.dump(
        {
            "quadruples": quadruples.getQuad(),
            "dirFunc": dirFunc,
            "constantsTable": constantsTable.getConstants()
        },
         handle, protocol=pickle.HIGHEST_PROTOCOL)


machine = vm.VirtualMachine()
machine.beginMachine()