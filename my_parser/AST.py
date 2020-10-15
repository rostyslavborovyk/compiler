from lexer.my_token import Token


class AST:
    def pprint(self, depth=0):
        pass


class NumAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumASTNode({self.token}, {self.value})"


class AssignExpAST(AST):
    def __init__(self, var_id, exp):
        self.var_id = var_id
        self.exp = exp

    def __repr__(self):
        return f"AssignExpAST(var_id={self.var_id}, exp={self.exp})"


class BinOpAST(AST):
    def __init__(self, left, op: Token, right):
        self.left: NumAST = left
        self.op = op
        self.right: NumAST = right

    def __repr__(self):
        return f"BinOpAST(op={self.op})"

    def pprint(self, depth=0):
        indent = "\t" * depth
        res = f"BinOpAST(\n" \
              f"\t{indent}op={self.op}\n" \
              f"\t{indent}left={self.left.pprint(depth + 1)}" \
              f"\t{indent}right={self.right.pprint(depth + 1)}" \
              f"{indent})\n"
        if depth == 0:
            print(res)
        return res


class UnOpAST(AST):
    def __init__(self, op: Token, right):
        self.op = op
        self.right: NumAST = right

    def pprint(self, depth=0):
        indent = "\t" * depth
        res = f"UnOpAST(\n" \
              f"\t{indent}op={self.op}\n" \
              f"\t{indent}right={self.right.pprint(depth + 1)}" \
              f"{indent})\n"
        if depth == 0:
            print(res)
        return res


class DecimalAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(DecimalAST, self).__init__(*args, **kwargs)

    def pprint(self, depth=0):
        indent = "\t" * depth
        res = f"DecimalAST(value={self.value})\n"

        if depth == 0:
            print(res)
        return res


class BinaryAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(BinaryAST, self).__init__(*args, **kwargs)


class StringAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"StringASTNode({self.token}, {self.value})"
