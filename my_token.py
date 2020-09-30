class Token:
    # token types
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    COLON = "COLON"
    BUILTIN_WORD = "BUILTIN_WORD"
    WORD = "WORD"
    SLASH_N = "SLASH_N"
    NUMBER_DECIMAL = "NUMBER_DECIMAL"
    NUMBER_BINARY = "NUMBER_BINARY"
    STRING = "STRING"

    BUILTIN_WORDS = (
        "def",
        "return"
    )

    def __init__(self, value, tok_type):
        self.value = value
        self.tok_type = tok_type

    def __repr__(self):
        return f'Token({self.tok_type}, {repr(self.value)})'
