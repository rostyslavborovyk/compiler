from lexer.my_token import Token


class AST:
    def prettyAST(self, depth=0):
        pass


class NumAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumASTNode({self.token}, {self.value})"


class StatementsListAST(AST):
    def __init__(self, children):
        self.children = children

    def prettyAST(self, depth=0):
        for child in self.children:
            print(child.prettyAST())


class AssignExpAST(AST):
    def __init__(self, var_id: Token, exp):
        self.var_id = var_id
        self.exp = exp

    def prettyAST(self, depth=0):
        indent = "\t" * depth
        res = f"AssignExpAST(\n" \
              f"\t{indent}var_id={self.var_id}\n" \
              f"\t{indent}exp={self.exp.prettyAST(depth + 1)}" \
              f"{indent})\n"
        return res

    def __repr__(self):
        return f"AssignExpAST(var_id={self.var_id}, exp={self.exp})"


class CondExpAST(AST):
    def __init__(self, cond, node_if, node_else):
        self.cond = cond
        self.node_if = node_if
        self.node_else = node_else

    def prettyAST(self, depth=0):
        indent = "\t" * depth
        res = f"CondExpAST(\n" \
              f"\t{indent}cond={self.cond.prettyAST(depth+1)}" \
              f"\t{indent}node_if={self.node_if.prettyAST(depth + 1)}" \
              f"\t{indent}node_else={self.node_else.prettyAST(depth + 1)}" \
              f"{indent})\n"
        return res


class IdAST(AST):
    def __init__(self, var_id: str):
        self.var_id = var_id

    def prettyAST(self, depth=0):
        return repr(self) + "\n"

    def __repr__(self):
        return f"IdAST(var_id={self.var_id})"


class BinOpAST(AST):
    def __init__(self, left, op: Token, right):
        self.left: NumAST = left
        self.op = op
        self.right: NumAST = right

    def __repr__(self):
        return f"BinOpAST(op={self.op})"

    def prettyAST(self, depth=0):
        indent = "\t" * depth
        res = f"BinOpAST(\n" \
              f"\t{indent}op={self.op}\n" \
              f"\t{indent}left={self.left.prettyAST(depth + 1)}" \
              f"\t{indent}right={self.right.prettyAST(depth + 1)}" \
              f"{indent})\n"
        return res


class UnOpAST(AST):
    def __init__(self, op: Token, right):
        self.op = op
        self.right: NumAST = right

    def prettyAST(self, depth=0):
        indent = "\t" * depth
        res = f"UnOpAST(\n" \
              f"\t{indent}op={self.op}\n" \
              f"\t{indent}right={self.right.prettyAST(depth + 1)}" \
              f"{indent})\n"
        return res


class DecimalAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(DecimalAST, self).__init__(*args, **kwargs)

    def prettyAST(self, depth=0):
        return repr(self) + "\n"

    def __repr__(self):
        return f"DecimalAST(value={self.value})"


class BinaryAST(NumAST):
    def __init__(self, *args, **kwargs):
        super(BinaryAST, self).__init__(*args, **kwargs)


class StringAST(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"StringASTNode({self.token}, {self.value})"
