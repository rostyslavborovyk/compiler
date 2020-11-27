from typing import List, Optional

from exceptions.my_exceptions import EOF, InvalidSyntaxException
from exceptions.my_exceptions import UnrecognizedTokenException
from lexer.my_token import Token
import re


class Lexer:
    """
    Returns list of tokens
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.cur_char: str = text[self.pos]

        self.row = 1  # row in which token is located
        self.row_pos = 0  # position in row

    def _set_next_char(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.cur_char = self.text[self.pos]
        else:
            self.cur_char = EOF
        self.row_pos += 1

    def _is_next_char(self, char):
        if self.pos + 1 == len(self.text):
            return False
        elif self.text[self.pos + 1] == char:
            return True

    def _skip_whitespace(self):
        if self.cur_char == " ":
            self._set_next_char()
        elif self.cur_char != EOF:
            raise UnrecognizedTokenException("Invalid token")

    def _validate_id_word(self, word) -> bool:
        """Validates id names, allowed chars are: all letters, underscores"""
        p = re.compile(r"[\w_]+")
        res = re.match(p, word)
        if not (res and len(res.group(0)) == len(word)):
            raise InvalidSyntaxException(f"Invalid variable name {word}")
        return True

    def _get_word(self) -> str:
        res = ""
        while (self.cur_char.isalpha() or self.cur_char == "_") and self.cur_char is not EOF:
            res += self.cur_char
            self._set_next_char()
        return res

    def _get_string(self) -> str:
        """
        Handles string in double quotes ("")
        """
        res = ""
        res += self.cur_char
        self._set_next_char()
        while self.cur_char != "\"" and self.cur_char is not EOF:
            res += self.cur_char
            self._set_next_char()
        res += self.cur_char
        self._set_next_char()
        return res

    def _get_multi_digit_num(self):
        """Returns num with one or more digits"""
        res = ""

        # handling binary number
        if self.cur_char == "0" and self._is_next_char("b"):
            res += self.cur_char  # appending "0"
            self._set_next_char()
            res += self.cur_char  # appending "b"
            self._set_next_char()
            while self.cur_char in "01":
                res += self.cur_char
                self._set_next_char()
            # self._skip_whitespace()
            return res

        # handling decimal number
        while self.cur_char.isdigit() and self.cur_char is not EOF:
            res += self.cur_char
            self._set_next_char()

        if self.cur_char == " ":
            self._skip_whitespace()
        return res

    def _get_special_symbols(self):
        res = self.text[self.pos]
        self._set_next_char()
        res += self.cur_char
        self._set_next_char()
        if res == "\\r":
            return None
        return res

    def handle_indents(self) -> List[Token]:
        # todo move indent var to global level
        tab_size = 4
        indent = " " * tab_size
        indents_ls = []
        while self.text[self.pos: self.pos + tab_size] == indent:
            indents_ls.append(Token(self.text[self.pos: self.pos + tab_size], Token.SLASH_T, (self.row, self.row_pos)))
            self.pos += tab_size
            self.cur_char = self.text[self.pos]
        return indents_ls

    def _process_comp_operations(self):
        lexeme_with_next_char = self.cur_char + self.text[self.pos + 1]
        if lexeme_with_next_char == Token.OPERATIONS["EQ"]:
            self._set_next_char()
            return Token(lexeme_with_next_char, Token.OPERATION, (self.row, self.row_pos))
        elif lexeme_with_next_char == Token.OPERATIONS["NEQ"]:
            self._set_next_char()
            return Token(lexeme_with_next_char, Token.OPERATION, (self.row, self.row_pos))
        elif lexeme_with_next_char == Token.OPERATIONS["GRE"]:
            self._set_next_char()
            return Token(lexeme_with_next_char, Token.OPERATION, (self.row, self.row_pos))
        elif lexeme_with_next_char == Token.OPERATIONS["LSE"]:
            self._set_next_char()
            return Token(lexeme_with_next_char, Token.OPERATION, (self.row, self.row_pos))

        elif self.cur_char == Token.OPERATIONS["GR"]:
            return Token(self.cur_char, Token.OPERATION, (self.row, self.row_pos))

        elif self.cur_char == Token.OPERATIONS["LS"]:
            return Token(self.cur_char, Token.OPERATION, (self.row, self.row_pos))

        return None

    def _process_comment(self):
        self._set_next_char()
        while self.cur_char != "\\" or not self._is_next_char("n"):
            self._set_next_char()

    def _process_assign_operations(self):
        lexeme_with_next_char = self.cur_char + self.text[self.pos + 1]
        if lexeme_with_next_char in Token.ASSIGNS.values():
            self._set_next_char()
            return Token(lexeme_with_next_char, Token.ASSIGN, (self.row, self.row_pos))
        return Token(self.cur_char, Token.OPERATION, (self.row, self.row_pos))

    def _get_token(self, lexeme) -> Token:
        """
        Returns token from given lexeme
        """
        tok_type = ""
        if lexeme == "(":
            tok_type = Token.L_BRACKET
        elif lexeme == ")":
            tok_type = Token.R_BRACKET
        elif lexeme == ":":
            tok_type = Token.COLON
        elif lexeme == ",":
            tok_type = Token.COMMA
        elif lexeme in Token.ASSIGNS.values():
            tok_type = Token.ASSIGN
        elif lexeme == "\\n":
            tok_type = Token.SLASH_N
            self.row_pos = 0
            self.row += 1
        elif lexeme[0] == "\"" and lexeme[-1]:  # todo (maybe) handle length
            tok_type = Token.STRING

        elif lexeme in Token.OPERATIONS.values():
            tok_type = Token.OPERATION

        # decimal number
        elif lexeme.isdigit():
            tok_type = Token.NUMBER_DECIMAL

        # binary number
        elif lexeme[:2] == "0b":
            tok_type = Token.NUMBER_BINARY

        # token for builtin names
        elif lexeme.isalpha() and lexeme in Token.BUILTIN_WORDS.values():
            tok_type = Token.BUILTIN_WORD

        # should be last
        # token for funcs and variables names
        elif self._validate_id_word(lexeme):
            tok_type = Token.ID

        if not tok_type:
            raise UnrecognizedTokenException(f"Unrecognized token: {lexeme}")

        return Token(lexeme, tok_type, (self.row, self.row_pos))

    def get_tokens(self):
        tokens_list: List[Token] = []
        while self.cur_char != EOF:
            if self.cur_char.isalpha() or self.cur_char == "_":
                # processing letters
                word = self._get_word()
                token = self._get_token(word)
                tokens_list.append(token)
            elif self.cur_char == "\"":
                string = self._get_string()
                token = self._get_token(string)
                tokens_list.append(token)
            elif self.cur_char.isdigit():
                number = self._get_multi_digit_num()
                token = self._get_token(number)
                tokens_list.append(token)
            elif self.cur_char == "\\":  # just normal \
                symbols = self._get_special_symbols()
                if symbols:
                    token = self._get_token(symbols)
                    tokens_list.append(token)
            elif self.cur_char == "(":
                token = self._get_token("(")
                tokens_list.append(token)
                self._set_next_char()
            elif self.cur_char == ")":
                token = self._get_token(")")
                tokens_list.append(token)
                self._set_next_char()
            elif self.cur_char == ":":
                token = self._get_token(":")
                tokens_list.append(token)
                self._set_next_char()
            elif self.cur_char == ",":
                token = self._get_token(",")
                tokens_list.append(token)
                self._set_next_char()
            elif self.cur_char in ("=", "!", ">", "<"):
                token = self._process_comp_operations()
                if token is not None:
                    tokens_list.append(token)
                    self._set_next_char()
                if token is None and self.cur_char == "=":
                    token = self._get_token("=")
                    tokens_list.append(token)
                    self._set_next_char()
            elif self.cur_char in Token.OPERATIONS.values():
                token = self._process_assign_operations()
                tokens_list.append(token)
                self._set_next_char()
            elif self.cur_char == "#":
                self._process_comment()
            elif self.cur_char == " ":
                indents = self.handle_indents()
                if indents:
                    tokens_list.extend(indents)
                else:
                    self._skip_whitespace()

        return tokens_list
