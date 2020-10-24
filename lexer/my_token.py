class Token:
    # token types
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    COLON = "COLON"
    BUILTIN_WORD = "BUILTIN_WORD"  # char sequence which corresponds to any BUILTIN_WORD
    OPERATION = "OPERATION"  # char sequence which corresponds to any BUILTIN_WORD
    ID = "ID"  # char sequence which not corresponds to any BUILTIN_WORD
    SLASH_N = "SLASH_N"
    SLASH_T = "SLASH_T"
    ASSIGN = "ASSIGN"
    NUMBER_DECIMAL = "NUMBER_DECIMAL"
    NUMBER_BINARY = "NUMBER_BINARY"
    STRING = "STRING"  # char sequence in ""

    BUILTIN_WORDS = {
        "DEF": "def",
        "RETURN": "return",
        "IF": "if",
        "ELSE": "else",
    }

    OPERATIONS = {
        "MINUS": "-",
        "PLUS": "+",
        "DIV": "/",
        "MUL": "*",
        "OR": "or",
    }

    def __init__(self, value, tok_type):
        self.value = value
        self.tok_type = tok_type

    def __repr__(self):
        return f'Token({self.tok_type}, {repr(self.value)})'
