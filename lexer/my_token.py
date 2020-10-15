class Token:
    # token types
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    COLON = "COLON"
    BUILTIN_WORD = "BUILTIN_WORD"  # char sequence which corresponds to any BUILTIN_WORD
    WORD = "WORD"  # char sequence which not corresponds to any BUILTIN_WORD
    SLASH_N = "SLASH_N"
    SLASH_T = "SLASH_T"
    ASSIGN = "="
    NUMBER_DECIMAL = "NUMBER_DECIMAL"
    NUMBER_BINARY = "NUMBER_BINARY"
    STRING = "STRING"  # char sequence in ""
    MINUS = "MINUS"
    DIV = "DIV"

    BUILTIN_WORDS = {
        "def": "def",
        "return": "return"
    }

    def __init__(self, value, tok_type):
        self.value = value
        self.tok_type = tok_type

    def __repr__(self):
        return f'Token({self.tok_type}, {repr(self.value)})'
