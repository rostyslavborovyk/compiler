from typing import List

# end of file
from AST import AST, StringAST, BinaryAST, DecimalAST
from my_exceptions import InvalidSyntaxException, EOF
from my_token import Token


class Parser:
    # todo modify expression to calculate arithmetic expressions
    """
    main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON (SLASH_N)? RETURN exp
    exp: exp binary_op exp | factor
    factor: unary_op factor | number | STRING
    number: DECIMAL | BINARY
    binary_op: DIV | MINUS
    unary_op: MINUS
    """

    def __init__(self, tokens_list):
        self.tokens_list: List[Token] = tokens_list
        self.pos = 0
        # set current token to the first token taken from the input
        self.current_token = self.tokens_list[self.pos]

    def _set_next_token(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens_list):
            self.current_token = self.tokens_list[self.pos]
        else:
            self.current_token = EOF

    def _check(self, tok_type, value=None) -> None:
        """
        Checks if cur_token of corresponding type, if so checks if value corresponds and sets the next token
        """
        # print(f"Checking token {tok_type} {f'with value {value}' if value else ''}")
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")
        if self.current_token.tok_type == tok_type:
            if value is not None and self.current_token.value == value:
                self._set_next_token()
                return
            elif value is not None and self.current_token.value != value:
                raise InvalidSyntaxException(
                    f"Token value {self.current_token.value} is wrong "
                    f"should be {value}"
                )
            self._set_next_token()
        else:
            raise InvalidSyntaxException(f"Token {self.current_token} should not be here")

    def _expression(self) -> AST:
        """
        expression: number | STRING, also == DECIMAL | BINARY | STRING
        """
        # while self.current_token != EOF:
        #     pass

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")
        node = None

        if self.current_token.tok_type == Token.STRING:
            node = StringAST(self.current_token)
        elif self.current_token.tok_type == Token.NUMBER_DECIMAL:
            node = DecimalAST(self.current_token)
        elif self.current_token.tok_type == Token.NUMBER_BINARY:
            node = BinaryAST(self.current_token)

        if node is None:
            raise InvalidSyntaxException("Wrong token in expression")

        return node

    def _main_func_expr(self) -> AST:
        """
        main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON (SLASH_N)? RETURN expression
        """
        self._check(Token.BUILTIN_WORD, "def")
        self._check(Token.WORD)
        self._check(Token.L_BRACKET)
        self._check(Token.R_BRACKET)
        self._check(Token.COLON)
        self._check(Token.SLASH_N)  # todo make presence of this token optional
        self._check(Token.BUILTIN_WORD, "return")
        node = self._expression()

        self._set_next_token()
        if self.current_token != EOF:
            raise InvalidSyntaxException("To much tokens for main function")

        return node

    def parse(self) -> AST:
        return self._main_func_expr()
