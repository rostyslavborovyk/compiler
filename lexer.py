from typing import List

from my_exceptions import EOF
from my_exceptions import UnrecognizedTokenException
from my_token import Token


class Lexer:
    """
    Returns list of tokens
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.cur_char: str = text[self.pos]

    def _set_next_char(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.cur_char = self.text[self.pos]
        else:
            self.cur_char = EOF

    def skip_whitespace(self):
        if self.cur_char == " ":
            self._set_next_char()
        elif self.cur_char != EOF:
            raise UnrecognizedTokenException("Invalid token")

    def _get_word(self) -> str:
        res = ""
        while self.cur_char.isalpha() and self.cur_char is not EOF:
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
        # todo process decimal and bin values
        res = ""

        # handling binary number
        if self.cur_char == "0" and self.text[self.pos + 1] == "b":
            res += self.cur_char  # appending "0"
            self._set_next_char()
            res += self.cur_char  # appending "b"
            self._set_next_char()
            while self.cur_char in "01":
                res += self.cur_char
                self._set_next_char()
            self.skip_whitespace()
            return res

        # handling decimal number
        while self.cur_char.isdigit() and self.cur_char is not EOF:
            res += self.cur_char
            self._set_next_char()
        self.skip_whitespace()
        return res

    def _get_special_symbols(self):
        res = self.text[self.pos]
        self._set_next_char()
        res += self.cur_char
        self._set_next_char()
        if res == "\\r":
            return None
        return res

    def _get_token(self, word):
        tok_type = ""
        if word == "(":
            tok_type = Token.L_BRACKET
        elif word == ")":
            tok_type = Token.R_BRACKET
        elif word == ":":
            tok_type = Token.COLON
        elif word == "\\n":
            tok_type = Token.SLASH_N
        elif word[0] == "\"" and word[-1]:  # todo (maybe) handle length
            tok_type = Token.STRING

        # decimal number
        elif word.isdigit():
            tok_type = Token.NUMBER_DECIMAL

        # binary number
        elif word[:2] == "0b":
            tok_type = Token.NUMBER_BINARY

        # token for builtin names
        elif word.isalpha() and word in Token.BUILTIN_WORDS:
            tok_type = Token.BUILTIN_WORD

        # should be last
        # token for funcs and variables names
        elif word.isalpha():
            tok_type = Token.WORD

        if not tok_type:
            raise UnrecognizedTokenException(f"Unrecognized token: {word}")

        return Token(word, tok_type)

    def get_tokens(self):
        tokens_list: List[Token] = []
        while self.cur_char != EOF:
            if self.cur_char.isalpha():
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
            elif self.cur_char == " ":
                self.skip_whitespace()

        return tokens_list
