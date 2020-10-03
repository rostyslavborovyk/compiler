from my_token import Token


class AST:
    def pprint(self, nesting=0):
        raise NotImplemented()


class NumAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.token}, {self.value})"

    def pprint(self, nesting=0):
        return "\t" * nesting + str(self)


class BinOpAST(AST):
    def __init__(self, left, op: Token, right):
        self.left: NumAST = left
        self.op = op
        self.right: NumAST = right

    def __repr__(self):
        return f"BinOpAST(op={self.op})"

    def pprint(self, nesting=0):
        base_indent = "\t" * nesting
        prettified = f"{base_indent}BinOpAST(\n{self.left.pprint(nesting + 1)}\n" \
                     f"{base_indent}\t{self.op}\n{self.right.pprint(nesting + 1)}\n{base_indent})"
        if nesting == 0:
            print(prettified)
        else:
            return prettified


class UnOpAST(AST):
    def __init__(self, op: Token, right):
        self.op = op
        self.right: NumAST = right

    def pprint(self, nesting=0):
        base_indent = "\t" * nesting
        prettified = f"{base_indent}UnOpAST(\n{base_indent}\t{self.op}" \
                     f"\n{self.right.pprint(nesting + 1)}\n{base_indent})"
        if nesting == 0:
            print(prettified)
        else:
            return prettified


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

    def pprint(self, nesting=0):
        pass
