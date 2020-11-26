from typing import List, Type

from my_parser.AST import AST, StringAST, DecimalAST, BinOpAST, UnOpAST, AssignExpAST, StatementsListAST, IdAST, \
    CondStatementAST, FunctionAST, FunctionCallAST, ProgramAST, WhileStatementAST, BreakStatementAST, \
    ContinueStatementAST, ReturnStatementAST, CompOpAST
from exceptions.my_exceptions import InvalidSyntaxException, EOF
from lexer.my_token import Token


class Parser:
    """
    program: func_expr* | func_call
    func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
    func_call: ID L_BRACKET top_level_exp (COMMA top_level_exp)* R_BRACKET
    statement_list: statement | statement SLASH_N SLASH_T* statement_list
    statement: assignment_statement | RETURN top_level_exp | conditional_statement
    | while_statement
    assignment_statement: ID ("=" | "*=") top_level_exp
    conditional_statement:
    IF top_level_exp COLON SLASH_N statement_list SLASH_T* ELSE COLON SLASH_N statement_list

    ========================== arithmetical expressions ===========================
    top_level_exp: exp_or
    exp_or: exp_comp (OR exp_comp)* | exp_comp
    exp_comp: exp ((EQ | NEQ | GR | LS | GRE | LSE) exp)* | exp
    exp: term ((MINUS | PLUS) term)* | term
    term: factor ((DIV | MUL | MOD) factor)* | factor
    factor: L_BRACKET top_level_exp R_BRACKET | unary_op | number | STRING | ID
    number: DECIMAL | BINARY
    unary_op: MINUS factor
    """

    def __init__(self, tokens_list):
        self.tokens_list: List[Token] = tokens_list
        self.pos = 0
        # set current token to the first token taken from the input
        self.current_token = self.tokens_list[self.pos]

    def parse(self) -> ProgramAST:
        return self._program()

    def _program(self) -> ProgramAST:
        """
        program: function_exr * | function_call
        """
        nesting = 0
        hl_statements = list()  # high level statements

        hl_statements.append(self._func_expr(nesting))

        while self._is_specific_token(Token.SLASH_N) or self._is_specific_token(Token.SLASH_T):
            self._check(self.current_token.tok_type)

        # if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["DEF"]):
        #     hl_statements.append(self._func_expr(nesting))
        #
        # while self._is_specific_token(Token.SLASH_N) or self._is_specific_token(Token.SLASH_T):
        #     self._check(self.current_token.tok_type)
        #
        # if self._is_specific_token(Token.ID):
        #     hl_statements.append(self._func_call())
        while self.current_token != EOF:
            if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["DEF"]):
                hl_statements.append(self._func_expr(nesting))

            if self._is_specific_token(Token.ID):
                hl_statements.append(self._func_call())

            while self._is_specific_token(Token.SLASH_N) or self._is_specific_token(Token.SLASH_T):
                self._check(self.current_token.tok_type)

        node = ProgramAST(hl_statements)

        return node

    def _func_expr(self, nesting: int) -> FunctionAST:
        """
        main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
        """
        func_id = None  # func_id won't be None anyway due to raised exceptions in _check methods
        func_args = []

        self._check_indent(nesting)
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["DEF"])

        if self._is_specific_token(Token.ID):
            func_id = self.current_token
            self._check(Token.ID)

        self._check(Token.L_BRACKET)
        if self._is_specific_token(Token.R_BRACKET):
            self._check(Token.R_BRACKET)

        elif self._is_specific_token(Token.ID):
            func_args.append(self.current_token)
            self._check(Token.ID)
            while self._is_specific_token(Token.COMMA):
                self._check(Token.COMMA)
                if self._is_specific_token(Token.ID):
                    func_args.append(self.current_token)
                    self._check(Token.ID)
                else:
                    raise InvalidSyntaxException(f"Here should be variable, not {self.current_token}")
            self._check(Token.R_BRACKET)
        # todo add processing of other args

        # self._check(Token.R_BRACKET)
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        # self._check(Token.SLASH_T)

        statement_list = self._statement_list(nesting + 1)
        node = FunctionAST(func_id, statement_list, func_args)

        return node

    def _func_call(self) -> FunctionCallAST:
        """
        func_call: ID L_BRACKET (top_level_exp | (top_level_exp (COMMA top_level_exp)*) R_BRACKET
        """
        func_id = self.current_token

        node = None
        self._check(Token.ID)
        self._check(Token.L_BRACKET)
        if self._is_specific_token(Token.R_BRACKET):
            self._check(Token.R_BRACKET)
            node = FunctionCallAST(func_id)
        elif self._is_specific_token(Token.ID) or self._is_specific_token(Token.NUMBER_DECIMAL):
            arg_list = [self.current_token]
            self._check(self.current_token.tok_type)
            while self._is_specific_token(Token.COMMA):
                self._check(Token.COMMA)
                if self._is_specific_token(Token.ID) or self._is_specific_token(Token.NUMBER_DECIMAL):
                    arg_list.append(self.current_token)
                    self._check(self.current_token.tok_type)
                else:
                    raise InvalidSyntaxException(f"Here should be variable or number, not {self.current_token}")

            self._check(Token.R_BRACKET)
            node = FunctionCallAST(func_id, arg_list)

        if node is None:
            raise InvalidSyntaxException(f"Wrong function call in function {func_id}")
        return node

    def _statement_list(self, nesting: int, is_cycle_body=False) -> Type[AST]:
        """
        statement_list: statement | statement SLASH_N SLASH_T* statement_list
        """

        self._check_indent(nesting)
        statements = [self._statement(nesting, is_cycle_body)]
        if not self._checkEOF():
            while self._is_specific_token(Token.SLASH_T) and self._is_in_previous_row():
                self._check(Token.SLASH_T)
            if self._is_specific_token(Token.SLASH_N):
                self._check(Token.SLASH_N)

        # todo set here check end of block
        if self._end_of_block(nesting):
            return StatementsListAST(statements)

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
                statements.append(self._statement(nesting, is_cycle_body))
                if self._end_of_block(nesting):
                    if self._is_specific_token(Token.SLASH_N):
                        self._check(Token.SLASH_N)
                    break
        return StatementsListAST(statements)

    def _statement(self, nesting: int, is_cycle_body=False) -> Type[AST]:
        """
        statement: assignment_statement | RETURN top_level_exp | conditional_statement
        | while_statement
        """
        node = None
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"]):
            node = self._return_statement()
        elif self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"]):
            node = self._conditional_statement(nesting, is_cycle_body)
        elif self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["WHILE"]):
            node = self._while_statement(nesting)
        elif is_cycle_body and self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["BREAK"]):
            node = self._break_statement()
        elif is_cycle_body and self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["CONTINUE"]):
            node = self._continue_statement()
        elif self._is_specific_token(Token.ID):  # todo set regexp to value to check var validity
            node = self._assignment_statement()

        if node is None:
            raise InvalidSyntaxException("Not matches with any statement")

        return node

    def _assignment_statement(self) -> AssignExpAST:
        """
        assignment_statement: ID ("=" | "*=" | "+=") top_level_exp
        """
        var_id = self.current_token
        self._check(Token.ID)

        if self._is_specific_token(Token.ASSIGN, Token.ASSIGNS["ASSIGN"]):
            self._check(Token.ASSIGN, Token.ASSIGNS["ASSIGN"])
            exp = self._top_level_exp()
        elif self._is_specific_token(Token.ASSIGN, Token.ASSIGNS["ASSIGN_MUL"]):
            self._check(Token.ASSIGN, Token.ASSIGNS["ASSIGN_MUL"])
            exp = BinOpAST(IdAST(var_id.value), Token("*", Token.OPERATION), self._top_level_exp())
        elif self._is_specific_token(Token.ASSIGN, Token.ASSIGNS["ASSIGN_SUM"]):
            self._check(Token.ASSIGN, Token.ASSIGNS["ASSIGN_SUM"])
            exp = BinOpAST(IdAST(var_id.value), Token("+", Token.OPERATION), self._top_level_exp())
        else:
            raise InvalidSyntaxException("Wrong token in factor expression")

        return AssignExpAST(var_id, exp)

    def _return_statement(self):
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"])
        return ReturnStatementAST(exp=self._top_level_exp())

    def _conditional_statement(self, nesting: int, is_cycle_body=False) -> CondStatementAST:
        """
        conditional_statement:
        IF top_level_exp COLON SLASH_N statement_list SLASH_T* ELSE COLON SLASH_N statement_list
        """
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"])
        cond_exp = self._top_level_exp()
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        node_if = self._statement_list(nesting + 1, is_cycle_body)
        if not self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["ELSE"]):
            self._check_indent(nesting)
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["ELSE"])
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        node_else = self._statement_list(nesting + 1, is_cycle_body)

        return CondStatementAST(cond_exp, node_if, node_else)

    def _while_statement(self, nesting) -> WhileStatementAST:
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["WHILE"])
        cond_exp = self._top_level_exp()
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        while_body = self._statement_list(nesting + 1, True)

        return WhileStatementAST(cond_exp, while_body)

    def _break_statement(self) -> BreakStatementAST:
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["BREAK"])
        return BreakStatementAST()

    def _continue_statement(self) -> ContinueStatementAST:
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["CONTINUE"])
        return ContinueStatementAST()

    def _top_level_exp(self) -> Type[AST]:
        node = None
        if self._is_specific_token(Token.ID) and self._is_next_specific_token(Token.L_BRACKET):
            node = self._func_call()
        else:
            node = self._exp_or()
        return node

    def _exp_or(self) -> Type[AST]:
        """
        exp_or: exp_comp (OR exp_comp)* | exp_comp
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._exp_comp()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (Token.OPERATIONS["OR"],):
            if token.value == Token.OPERATIONS["OR"]:
                self._check(Token.OPERATION, Token.OPERATIONS["OR"])

            node = BinOpAST(node, token, self._exp_comp())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"in exp_or"
            )

        return node

    def _exp_comp(self) -> Type[AST]:
        """
        exp_comp: exp ((EQ | NEQ | GR | LS | GRE | LSE) exp)* | exp
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = self._expression()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (
                Token.OPERATIONS["EQ"],
                Token.OPERATIONS["NEQ"],
                Token.OPERATIONS["GR"],
                Token.OPERATIONS["LS"],
                Token.OPERATIONS["GRE"],
                Token.OPERATIONS["LSE"],
        ):
            self._check(token.tok_type)

            node = CompOpAST(node, token, self._expression())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"in exp_comp"
            )

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
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (
                Token.OPERATIONS["MINUS"], Token.OPERATIONS["PLUS"]):
            if token.value == Token.OPERATIONS["MINUS"]:
                self._check(Token.OPERATION, Token.OPERATIONS["MINUS"])
            elif token.value == Token.OPERATIONS["PLUS"]:
                self._check(Token.OPERATION, Token.OPERATIONS["PLUS"])
            node = BinOpAST(node, token, self._term())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"in expression"
            )

        return node

    def _term(self) -> Type[AST]:
        """
        term: factor ((DIV | MUL | MOD) factor)* | factor
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        # node = None

        node = self._factor()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (
                Token.OPERATIONS["DIV"], Token.OPERATIONS["MUL"], Token.OPERATIONS["MOD"]):
            if token.value == Token.OPERATIONS["DIV"]:
                self._check(Token.OPERATION, Token.OPERATIONS["DIV"])
            elif token.value == Token.OPERATIONS["MUL"]:
                self._check(Token.OPERATION, Token.OPERATIONS["MUL"])
            elif token.value == Token.OPERATIONS["MOD"]:
                self._check(Token.OPERATION, Token.OPERATIONS["MOD"])
            node = BinOpAST(node, token, self._factor())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                "in term expression"
            )

        return node

    def _factor(self) -> Type[AST]:
        """
        factor: L_BRACKET top_level_exp R_BRACKET | unary_op | number | STRING | ID
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        token = self.current_token

        if token.tok_type == Token.L_BRACKET:
            self._check(Token.L_BRACKET)
            node = self._top_level_exp()
            self._check(Token.R_BRACKET)

        if token.tok_type == Token.OPERATION and token.value == Token.OPERATIONS["MINUS"]:
            self._check(Token.OPERATION, Token.OPERATIONS["MINUS"])
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
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")
        elif not self._is_specific_token(tok_type, value):
            raise InvalidSyntaxException(
                f"Token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"should not be here"
            )
        else:
            self._set_next_token()

    def _is_specific_token(self, tok_type, value=None, token=None) -> bool:
        token = token if token else self.current_token

        if token == EOF:
            return False
        if token.tok_type == tok_type:
            if value is not None and token.value == value:
                return True
            elif value is not None and token.value != value:
                return False
            return True
        else:
            return False

    def _is_next_specific_token(self, tok_type, value=None) -> bool:
        next_token = self.tokens_list[self.pos + 1]
        return self._is_specific_token(tok_type, value, next_token)

    def _check_indent(self, nesting: int):
        for i in range(nesting):
            self._check(Token.SLASH_T)

    def _is_statement(self) -> bool:
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"]) \
                or self._is_specific_token(Token.ID) \
                or self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"]) \
                or self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["WHILE"]) \
                or self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["BREAK"]) \
                or self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["CONTINUE"]):
            return True
        return False

    def _is_in_previous_row(self):
        token = self.current_token
        pos_offset = 0
        while True:
            while token.tok_type == Token.SLASH_T:
                pos_offset += 1
                token = self.tokens_list[self.pos + pos_offset]
            if token.tok_type == Token.SLASH_N:
                return True
            else:
                return False

    def _end_of_block(self, nesting):
        if self.current_token == EOF:
            return True
        pos = self.pos
        token = self.tokens_list[pos]
        # if token.tok_type != Token.SLASH_N:
        #     return True

        # pos += 1
        # token = self.tokens_list[pos]
        if token.tok_type == Token.SLASH_N:
            pos += 1
            token = self.tokens_list[pos]

        for i in range(nesting):
            if token.tok_type != Token.SLASH_T:
                return True
            pos += 1
            token = self.tokens_list[pos]
        return False
