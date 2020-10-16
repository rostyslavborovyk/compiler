from typing import List, Type

from my_parser.AST import AST, StringAST, DecimalAST, BinOpAST, UnOpAST, AssignExpAST, StatementsListAST, IdAST
from exceptions.my_exceptions import InvalidSyntaxException, EOF
from lexer.my_token import Token


class Parser:
    """
    main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N SLASH_T statement_list
    statement_list: statement | statement SLASH_N SLASH_T* statement_list
    statement: assignment_statement | RETURN exp
    assignment_statement: ID "=" exp
    exp: term (MINUS term)* | term  # "+" and other low priority operators can be added here
    term: factor (DIV factor)* | factor  # "*" and other high priority operators can be added here
    factor: L_BRACKET exp R_BRACKET | unary_op factor | number | STRING | ID
    number: DECIMAL | BINARY
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

    # def _is_unary_op(self):
    #     if self.current_token.tok_type in (Token.MINUS,):
    #         return True
    #     return False

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
                return None
            elif value is not None and self.current_token.value != value:
                raise InvalidSyntaxException(
                    f"Token value {self.current_token.value} is wrong "
                    f"should be {value}"
                )
            self._set_next_token()
        else:
            raise InvalidSyntaxException(f"Token {self.current_token} should not be here")

    def _is_specific_token(self, tok_type, value=None) -> bool:
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")
        if self.current_token.tok_type == tok_type:
            if value is not None and self.current_token.value == value:
                return True
            elif value is not None and self.current_token.value != value:
                return False
            return True
        else:
            return False

    def _factor(self) -> Type[AST]:
        """
        factor: L_BRACKET exp R_BRACKET | unary_op factor | number | STRING | ID
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        token = self.current_token

        if token.tok_type == Token.L_BRACKET:
            self._check(Token.L_BRACKET)
            node = self._expression()
            self._check(Token.R_BRACKET)

        if token.tok_type == Token.MINUS:
            self._check(Token.MINUS)
            node = UnOpAST(token, self._factor())

        elif token.tok_type == Token.NUMBER_DECIMAL:  # todo maybe handle binary num too
            self._check(Token.NUMBER_DECIMAL)
            node = DecimalAST(token)

        elif token.tok_type == Token.STRING:
            self._check(Token.STRING)
            node = StringAST(self.current_token)

        elif token.tok_type == Token.ID:
            self._check(Token.ID)
            node = IdAST(token.value)

        if node is None:
            raise InvalidSyntaxException("Wrong token in factor expression")

        return node

    def _term(self) -> Type[AST]:
        """
        term: factor (DIV factor)* | factor  # "*" and other high priority operators can be added here
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        # node = None

        node = self._factor()
        token = self.current_token
        while self.current_token != EOF and self.current_token.tok_type in (Token.DIV,):
            if token.tok_type == Token.DIV:
                self._check(Token.DIV)
            node = BinOpAST(node, token, self._factor())

        if node is None:
            raise InvalidSyntaxException("Wrong token in term expression")

        return node

    def _expression(self) -> Type[AST]:
        """
        exp: term (MINUS term)* | term  # "+" and other low priority operators can be added here
        """
        # while self.current_token != EOF:
        #     pass

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._term()
        token = self.current_token
        while self.current_token != EOF and self.current_token.tok_type in (Token.MINUS,):
            if token.tok_type == Token.MINUS:
                self._check(Token.MINUS)
            # some more operations ...

            node = BinOpAST(node, token, self._term())

        if node is None:
            raise InvalidSyntaxException("Wrong token in expression")

        return node

    def _assignment_statement(self) -> Type[AST]:
        """
        assignment_statement: ID "=" exp
        """
        var_id = self.current_token
        self._check(Token.ID)
        self._check(Token.ASSIGN)
        exp = self._expression()

        return AssignExpAST(var_id, exp)

    def _statement(self) -> Type[AST]:
        """
        statement: assignment_statement | RETURN exp
        """
        node = None
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["return"]):
            self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["return"])
            node = self._expression()
        elif self._is_specific_token(Token.ID):  # todo set regexp to value to check var validity
            node = self._assignment_statement()

        if node is None:
            raise InvalidSyntaxException("Not matches with any statement")

        return node

    def _statement_list(self) -> Type[AST]:
        """
        statement_list: statement | statement SLASH_N SLASH_T* statement_list
        """
        statements = [self._statement()]

        while self.current_token != EOF:
            # handle new line
            while self.current_token.tok_type == Token.SLASH_N:
                self._check(Token.SLASH_N)

            # handle indent
            if self.current_token.tok_type == Token.SLASH_T:
                self._check(Token.SLASH_T)
            statements.append(self._statement())
        node = StatementsListAST(statements)
        return node

    def _main_func_expr(self) -> Type[AST]:
        """
        main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N SLASH_T statement_list
        """
        self._check(Token.BUILTIN_WORD, "def")
        self._check(Token.ID)
        self._check(Token.L_BRACKET)
        self._check(Token.R_BRACKET)
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        self._check(Token.SLASH_T)
        # self._check(Token.BUILTIN_WORD, "return")
        # node = self._expression()
        node = self._statement_list()
        # while self.current_token != EOF:
        #     node = self._line_expression()
        self._set_next_token()
        if self.current_token != EOF:
            raise InvalidSyntaxException("To much tokens for main function")

        return node

    def parse(self) -> Type[AST]:
        return self._main_func_expr()
