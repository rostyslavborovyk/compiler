from my_token import Token


class AST:
    pass


class NumAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumASTNode({self.token}, {self.value})"


class BinOpAST(AST):
    def __init__(self, left, op, right):
        self.left: NumAST = left
        self.token = self.op = op
        self.right: NumAST = right


class DecimalAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(DecimalAST, self).__init__(*args, **kwargs)


class BinaryAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(BinaryAST, self).__init__(*args, **kwargs)


class StringAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"StringASTNode({self.token}, {self.value})"
