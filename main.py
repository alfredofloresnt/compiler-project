
import ply.lex as lex
import ply.yacc as yacc

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



# YACC
def p_PROGRAM(p):
    '''program : PROGRAM ID SEMICOLON program2
               | PROGRAM ID SEMICOLON program3
               | PROGRAM ID SEMICOLON program4
       program2 : decVars program3
                | decVars program4
       program3 : functions program4
       program4 : MAIN LPAREN RPAREN block'''

def p_DEC_VARS(p):
    '''decVars : VARS decVars2
       decVars2 : type TWOPOINTS decVars3
       decVars3 : ID decVars4
                | ID decVars5
                | ID decVars6
       decVars4 : COMMA decVars3
       decVars5 : LSQUAREBRACKET cteint RSQUAREBRACKET decVars4
                | LSQUAREBRACKET cteint RSQUAREBRACKET decVars6
       decVars6 : SEMICOLON decVars2
                | SEMICOLON'''
    
def p_FUNCTIONS(p):
    '''functions : function functions
                | function'''
    
def p_FUNCTION(p):
    '''function : FUNCTION type ID LPAREN param RPAREN decVars block
                | FUNCTION VOID ID LPAREN param RPAREN decVars block'''

def p_PARAM(p):
    '''param : type TWOPOINTS ID empty
             | type TWOPOINTS ID COMMA param'''


def p_TYPE(p):
    '''type : INT
            | FLOAT
            | CHAR'''

def p_BLOCK(p):
    '''block : LBRACKET block2
       block2 : block3
               | block4
       block3 : statement block2
       block4 : RBRACKET'''

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
    '''assignation : variable EQUAL expression SEMICOLON'''

def p_VARIABLE(p):
    '''variable : ID variable2
                | ID
       variable2 : LSQUAREBRACKET variable3 RSQUAREBRACKET
       variable3 : expression'''
        
def p_PRINT_ON_SCREEN(p):
    '''print : PRINT LPAREN print2
       print2 : expression print3
                  | ctestring print3
       print3 : COMMA print2
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
    '''expression : exp
                 | exp RELOP exp'''

def p_CONDITION(p):
    '''condition : IF LPAREN expression RPAREN block
            | IF LPAREN expression RPAREN block ELSE block'''

def p_FUNCTION_CALL(p):
    '''functionCall : ID LPAREN functionCall2
                    | ID LPAREN RPAREN
       functionCall2 : expression RPAREN
                     | expression COMMA functionCall2'''

def p_EXP(p):
    '''exp : term exp2
       exp2 : OPERATORTYPE1 exp
            | empty'''

def p_TERM(p):
    '''term : factor term2
       term2 : OPERATORTYPE2 term
             | empty'''

def p_FACTOR(p):
    '''factor : LPAREN expression RPAREN
              | factor2 varcte
              | factor3
       factor2 : OPERATORTYPE1
               | empty
        factor3 : ID
                | ID LPAREN factor4
                | ID LSQUAREBRACKET factor5
        factor4 : expression COMMA factor4
                | expression RPAREN
        factor5 : expression COMMA factor5
                | expression RSQUAREBRACKET'''

def p_VARCTE(p):
    '''varcte : ID
              | cteint
              | ctefloat
              | ctechar'''

def p_EMPTY(p):
    '''empty :'''
    pass


def p_error(t):
    print("Error (Syntax):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")


codeToCompile = open('code.txt','r')
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
    print('Code passed!')
except:
    print('Error in code!')