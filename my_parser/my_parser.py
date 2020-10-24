from typing import List, Type

from my_parser.AST import AST, StringAST, DecimalAST, BinOpAST, UnOpAST, AssignExpAST, StatementsListAST, IdAST
from exceptions.my_exceptions import InvalidSyntaxException, EOF
from lexer.my_token import Token


class Parser:
    """
    main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
    statement_list: statement | statement SLASH_N SLASH_T* statement_list
    statement: assignment_statement | RETURN exp_logical
    assignment_statement: ID "=" exp_logical
    exp_logical: exp (OR exp)* | exp
    exp: term ((MINUS | PLUS) term)* | term
    term: factor ((DIV | MUL) factor)* | factor
    factor: L_BRACKET exp_logical R_BRACKET | unary_op factor | number | STRING | ID
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

    def _checkEOF(self):
        if self.current_token == EOF:
            return True
        return False

    def _check(self, tok_type, value=None) -> None:
        """
        Checks if cur_token of corresponding type, if so checks if value corresponds and sets the next token
        """
        # print(f"Checking token {tok_type} {f'with value {value}' if value else ''}")
        if self._checkEOF():
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

    def _check_indent(self, nesting: int):
        for i in range(nesting):
            self._check(Token.SLASH_T)

    def _is_specific_token(self, tok_type, value=None) -> bool:
        if self.current_token == EOF:
            return False
        if self.current_token.tok_type == tok_type:
            if value is not None and self.current_token.value == value:
                return True
            elif value is not None and self.current_token.value != value:
                return False
            return True
        else:
            return False

    def _is_statement(self) -> bool:
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["return"]) \
                or self._is_specific_token(Token.ID):
            return True
        return False

    def _factor(self) -> Type[AST]:
        """
        factor: L_BRACKET exp_logical R_BRACKET | unary_op factor | number | STRING | ID
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        token = self.current_token

        if token.tok_type == Token.L_BRACKET:
            self._check(Token.L_BRACKET)
            node = self._exp_logical()
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
        term: factor ((DIV | MUL) factor)* | factor
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        # node = None

        node = self._factor()
        token = self.current_token
        while self.current_token != EOF and self.current_token.tok_type in (Token.DIV, Token.MUL):
            if token.tok_type == Token.DIV:
                self._check(Token.DIV)
            elif token.tok_type == Token.MUL:
                self._check(Token.MUL)
            node = BinOpAST(node, token, self._factor())

        if node is None:
            raise InvalidSyntaxException("Wrong token in term expression")

        return node

    def _expression(self) -> Type[AST]:
        """
        exp: term ((MINUS | PLUS) term)* | term
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._term()
        token = self.current_token
        while self.current_token != EOF and self.current_token.tok_type in (Token.MINUS, Token.PLUS):
            if token.tok_type == Token.MINUS:
                self._check(Token.MINUS)
            elif token.tok_type == Token.PLUS:
                self._check(Token.PLUS)
            node = BinOpAST(node, token, self._term())

        if node is None:
            raise InvalidSyntaxException("Wrong token in expression")

        return node

    def _exp_logical(self) -> Type[AST]:
        """
        exp_logical: exp (OR exp)* | exp
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._expression()
        token = self.current_token
        while self.current_token != EOF and self.current_token.value in (Token.BUILTIN_WORDS["or"],):
            if token.tok_type == Token.BUILTIN_WORD and token.value == Token.BUILTIN_WORDS["or"]:
                self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["or"])

            node = BinOpAST(node, token, self._expression())

        if node is None:
            raise InvalidSyntaxException("Wrong token in expression")

        return node

    def _assignment_statement(self) -> Type[AST]:
        """
        assignment_statement: ID "=" exp_logical
        """
        var_id = self.current_token
        self._check(Token.ID)
        self._check(Token.ASSIGN)
        exp = self._exp_logical()

        return AssignExpAST(var_id, exp)

    def _statement(self) -> Type[AST]:
        """
        statement: assignment_statement | RETURN exp_logical
        """
        node = None
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["return"]):
            self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["return"])
            node = self._exp_logical()
        elif self._is_specific_token(Token.ID):  # todo set regexp to value to check var validity
            node = self._assignment_statement()

        if node is None:
            raise InvalidSyntaxException("Not matches with any statement")

        return node

    def _statement_list(self, nesting: int) -> Type[AST]:
        """
        statement_list: statement | statement SLASH_N SLASH_T* statement_list
        """

        self._check_indent(nesting)
        statements = [self._statement()]
        if not self._checkEOF():
            while self._is_specific_token(Token.SLASH_T):
                self._check(Token.SLASH_T)
            self._check(Token.SLASH_N)

        while not self._checkEOF():
            # handle new line
            # if self.current_token.tok_type == Token.SLASH_N:
            while self._is_specific_token(Token.SLASH_N):
                while self._is_specific_token(Token.SLASH_T):
                    self._check(Token.SLASH_T)
                self._check(Token.SLASH_N)
            if self._checkEOF():
                break
            self._check_indent(nesting)
            if self._checkEOF():
                break
            if self._is_statement():
                statements.append(self._statement())

        node = StatementsListAST(statements)
        return node

    def _func_expr(self, nesting: int) -> Type[AST]:
        """
        main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
        """
        self._check_indent(nesting)
        self._check(Token.BUILTIN_WORD, "def")
        self._check(Token.ID)
        self._check(Token.L_BRACKET)
        self._check(Token.R_BRACKET)
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        # self._check(Token.SLASH_T)

        node = self._statement_list(nesting + 1)

        return node

    def _program(self) -> Type[AST]:
        nesting = 0

        node = self._func_expr(nesting)

        # self._set_next_token()
        if self.current_token != EOF:
            raise InvalidSyntaxException("To much tokens for main function")

        return node

    def parse(self) -> Type[AST]:
        return self._program()
