from typing import Tuple


class Token:
    # token types
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    COLON = "COLON"
    BUILTIN_WORD = "BUILTIN_WORD"  # char sequence which corresponds to any BUILTIN_WORD
    OPERATION = "OPERATION"  # char sequence which corresponds to any OPERATION
    ID = "ID"  # char sequence which not corresponds to any BUILTIN_WORD or OPERATION
    SLASH_N = "SLASH_N"
    SLASH_T = "SLASH_T"
    ASSIGN = "ASSIGN"
    NUMBER_DECIMAL = "NUMBER_DECIMAL"
    NUMBER_BINARY = "NUMBER_BINARY"
    STRING = "STRING"  # char sequence in ""

    # token values
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

    ASSIGNS = {
        "ASSIGN": "=",
        "ASSIGN_MUL": "*=",
    }

    def __init__(self, value, tok_type, pos: Tuple[int, int] = None):
        self.value = value
        self.tok_type = tok_type

        # (row, position_in_row)
        self.pos = pos

    def __repr__(self):
        return f'Token(tok_type={self.tok_type}, value={repr(self.value)}, pos=({self.pos}))'
