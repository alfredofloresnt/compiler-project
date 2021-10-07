# Semantic cube definition
semantic = {
    "int": {
        "int": {
            "+": "int",
            "-": "int",
            "*": "float",
            "/": "float",
            ">": "boolean",
            "<": "boolean",
            "<>": "boolean",
        },
        "float": {

        },
        "boolean": {
            
        }
    
    }
}

# Semantic cube access
def getType(leftOperandType, rightOperandType, operation):
    # Check if left and right operand type exist also operation else error
    if (semantic.has_key(leftOperandType) and semantic[leftOperandType].has_key(rightOperand) and semantic[leftOperandType][rightOperandType].has_key(operation)):
        return semantic[leftOperandType][rightOperandType][operation]
    else:
        return None # Equals to error
