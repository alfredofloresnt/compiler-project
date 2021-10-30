
import ply.lex as lex
import ply.yacc as yacc
import varTables as vt
import quadruples as qp
import semanticCube as sc
import random

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
    'return': 'RETURN'
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
          'SEMICOLON',
          'COMMA'] + list(reserved.values())

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
t_RELOP = r'\<\>|\<|\>|\=\='
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
t_SEMICOLON = r';'
t_COMMA = r','
t_ignore = ' '

def t_ctefloat(t):
    r'([0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_cteint(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ctechar(t):
    r'^[a-zA-Z]+$'
    t.value = int(t.value)
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
currentType = None
currentVarTable = None
globalFunctionName = None
quadruples = qp.Quadruples()

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
    '''program4 : MAIN LPAREN RPAREN block'''

def p_DEC_VARS(p):
    '''decVars : VARS np3CreateVarsTable decVars2'''   

def p_DEC_VARS2(p):
    '''decVars2 : type TWOPOINTS decVars3'''
    
def p_DEC_VARS3(p):
    '''decVars3 : ID np4AddCurrentTable decVars4
                | ID np4AddCurrentTable decVars5
                | ID np4AddCurrentTable decVars6'''

def p_DEC_VARS4(p):
    '''decVars4 : COMMA decVars3'''

def p_DEC_VARS5(p):
    '''decVars5 : LSQUAREBRACKET cteint RSQUAREBRACKET decVars4
                | LSQUAREBRACKET cteint RSQUAREBRACKET decVars6'''

def p_DEC_VARS6(p):
    '''decVars6 : SEMICOLON decVars2
                | SEMICOLON'''
    
    
def p_FUNCTIONS(p):
    '''functions : function functions
                | function'''
    
def p_FUNCTION(p):
    '''function : FUNCTION type ID np9AddFunction np3CreateVarsTable LPAREN param RPAREN decVars block np12DeleteCurrentVarsTable
                | FUNCTION VOID np8SetCurrentTypeVoid ID np9AddFunction np3CreateVarsTable LPAREN param RPAREN decVars block np12DeleteCurrentVarsTable'''

def p_PARAM(p):
    '''param : type TWOPOINTS ID np4AddCurrentTable empty
             | type TWOPOINTS ID np4AddCurrentTable COMMA param'''


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
                | functionCall
                | forLoop
                | returnFunc'''

def p_ASSIGNATION(p):
    '''assignation : variable EQUAL qnp2_push_operations expression assigmentnp SEMICOLON'''

def p_VARIABLE(p):
    '''variable : ID qnp1_push variable2
                | ID qnp1_push'''

def p_VARIABLE2(p):
    '''variable2 : LSQUAREBRACKET variable3 RSQUAREBRACKET'''

def p_VARIABLE3(p):
    '''variable3 : expression'''
        
def p_PRINT_ON_SCREEN(p):
    '''print : PRINT LPAREN print2'''

def p_PRINT_ON_SCREEN2(p):
    '''print2 : expression print3
              | ctestring print3'''

def p_PRINT_ON_SCREEN3(p):
    '''print3 : COMMA print2
              | RPAREN SEMICOLON'''

def p_WHILE_LOOP(p):
    '''whileLoop : WHILE LPAREN expression RPAREN block'''

def p_FOR_LOOP(p):
    '''forLoop : FOR LPAREN ID EQUAL exp TO exp RPAREN block'''

def p_RETURN_FUNC(p):
    '''returnFunc : RETURN LPAREN expression RPAREN SEMICOLON'''

def p_READ_INPUT(p):
    '''readInput : READ LPAREN variable RPAREN SEMICOLON'''

def p_EXPRESSION(p):
    '''expression : exp qnp6_push_operationtypeRELOP_apply
                 | exp RELOP qnp2_push_operations exp qnp6_push_operationtypeRELOP_apply'''

def p_CONDITION(p):
    '''condition : IF LPAREN expression ifnp1 RPAREN block ifnp2End
                 | IF LPAREN expression ifnp1 RPAREN block ELSE ifnp3Else block ifnp2End'''
    


def p_FUNCTION_CALL(p):
    '''functionCall : ID LPAREN functionCall2
                    | ID LPAREN RPAREN'''

def p_FUNCTION_CALL2(p):
    '''functionCall2 : expression RPAREN
                     | expression COMMA functionCall2'''

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
    '''factor : LPAREN expression RPAREN
              | factor2 varcte
              | factor3'''

def p_FACTOR2(p):
    '''factor2 : OPERATORTYPE1
               | empty'''

def p_FACTOR3(p):
    '''factor3 : ID qnp1_push
                | ID qnp1_push LPAREN factor4
                | ID qnp1_push LSQUAREBRACKET factor5'''

def p_FACTOR4(p):
    '''factor4 : expression COMMA factor4
                | expression RPAREN'''

def p_FACTOR5(p):
    '''factor5 : expression COMMA factor5
                | expression RSQUAREBRACKET'''

def p_VARCTE(p):
    '''varcte : ID
              | cteint
              | ctefloat
              | ctechar'''

def p_EMPTY(p):
    '''empty :'''
    pass

# Neuralgic points

def p_TEST(p):
    '''np0Test : empty'''
    print("BBBB")
    quadruples.printStacks()

def p_NP2_CREATE_MAIN_VARS_TABLE(p):
    '''np2CreateMainVarsTable : empty'''
    global dirFunc
    global currentFunc
    global globalFunctionName
    dirFunc = vt.DirFunc()
    dirFunc.insert({"name": p[-1], "type": "global", "table": None})
    globalFunctionName = p[-1]
    currentFunc = p[-1]

def p_NP3_CREATE_VARS_TABLE(p):
    '''np3CreateVarsTable : empty'''
    global dirFunc
    global currentVarTable
    row = dirFunc.getFunctionByName(currentFunc)
    if (row["table"] == None):
        currentVarTable = vt.Vars()
        dirFunc.addVarsTable(currentFunc, currentVarTable)
        

def p_NP4_ADD_CURRENT_TABLE(p):
    '''np4AddCurrentTable : empty'''
    global currentVarTable
    global currentType
    # Check if id-name in current VarsTable
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        print("Semantic Error: Multiple variable declaration of " + p[-1])
    else:
        currentVarTable.insert({"name": p[-1], "type": currentType})

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
        print("Semantic Error: Multiple function declaration of " + p[-1])
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
def p_QNP1_PUSH(p):
    '''qnp1_push : empty'''
    quadruples.getOperandsStack().push(p[-1])
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

def quadruplesProcess():
    print("ENTER PROCESS")
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
        result = random.randint(0, 999) # This line has to be modified in the future. Addressing needs to be implemented
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
        if (quadruples.getOperationsStack().top() == ">" or quadruples.getOperationsStack().top() == "<" or quadruples.getOperationsStack().top() == "<>" or quadruples.getOperationsStack().top() == "<=" or quadruples.getOperationsStack().top() == ">="):
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
    resIDType = sc.getType(idType, resType, '=')
    if (equalSymbol == "=" and resIDType == "valid"):
        quadruples.generateQuad(equalSymbol, result, 'empty', id)
    else:
        print("Semantic Error: Type mismatch", resType, "cannot be", idType)
        
# Neuralgic point for IF statement
def p_IFNP1(p):
    '''ifnp1 : empty'''
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (expType != 'boolean'):
        print("Semantic Error: Type mismatch, not boolean")
    else:
        result = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad('GoToF', result, 'empty', None)
        cont = quadruples.getQuad().size() + 1
        quadruples.getJumpsStack().push(cont - 1)

def p_IFNP2_END(p):
    '''ifnp2End : empty'''
    print("IF END")
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

def p_RELOP_ADD(p):
    '''relopnp : empty'''
    quadruples.getOperationsStack().push(p[-1])

# Neuralgic point for WHILE statement
def p_WHILENP1(p):
    '''ifnpWhile1 : empty'''
    cont = quadruples.getQuad().size()
    quadruples.getJumpsStack().push(cont)

def p_WHILENP2(p):
    '''ifnpWhile2 : empty'''
    expType = quadruples.getTypeStack().top()
    quadruples.getTypeStack().pop()
    if (expType != 'boolean'):
        print("Semantic Error: Type mismatch")
    else:
        result = quadruples.getOperandsStack().top()
        quadruples.getOperandsStack().pop()
        quadruples.generateQuad('GoToF', result, 'empty', None)
        cont = quadruples.getQuad().size()
        quadruples.getJumpsStack().push(cont - 1)

def p_WHILENP3(p):
    '''ifnpWhile3 : empty'''
    end = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    ret = quadruples.getJumpsStack().top()
    quadruples.getJumpsStack().pop()
    cont = quadruples.getQuad().size()
    quadruples.generateQuad('GoTo', 'empty', 'empty', ret)
    quadruples.fillQuad(end, cont)

# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")


codeToCompile = open('code3.txt','r')
data = str(codeToCompile.read())
lexer.input(data)
# Debug tokens
#while True:
#    tok = lexer.token()
#    if not tok: 
#        break # No more input
#    print(tok)
try:
    
    parser.parse(data)
    quadruples.printQuads()
    # dirFunc.printDirFunc()
    print('Code passed!')
except Exception as e:
    print('Error in code!', e)