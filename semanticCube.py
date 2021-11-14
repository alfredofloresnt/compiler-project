# Semantic cube access
def getType(leftOperandType, rightOperandType, operation):
    # Check if left and right operand type exist also operation else error
    if (leftOperandType in semantic and rightOperandType in semantic[leftOperandType] and operation in semantic[leftOperandType][rightOperandType]):
        return semantic[leftOperandType][rightOperandType][operation]
    else:
        return None # Equals to error

# Semantic cube definition
semantic = {
    "int": {
        "int": {
            "+": "int",
            "-": "int",
            "*": "int",
            "/": "int",
            "=": "valid",
            ">": "int",
            ">=": "int",
            "<": "int",
            ">=": "int",
            "<>": "int",
            "==": 'int',
            "&&": "int",
            "||": "int"
        },
        "float": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            ">": "int",
            ">=": "int",
            "<": "int",
            ">=": "int",
            "<>": "int",
            "==": 'int'
        } 
    },
    "float": {
        "int": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            "=": "valid",
            ">": "int",
            ">=": "int",
            "<": "int",
            ">=": "int",
            "<>": "int",
            "==": 'int'
        },
        "float": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            "=": "valid",
            ">": "int",
            ">=": "int",
            "<": "int",
            ">=": "int",
            "<>": "int",
            "==": 'int'
        } 
    },
    "char": {
        "char": {
            "=": "valid",
            "<>": "int",
            "==": 'int'
        }
    }
}