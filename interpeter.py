from AST import AST, NumAST, StringAST, BinOpAST, UnOpAST, DecimalAST
from typing import Union

from code_generator import CodeGenerator
from my_exceptions import NoVisitMethodException
from my_token import Token


class Interpreter:
    def __init__(self, ast: Union[NumAST, StringAST]):
        self.code_generator = CodeGenerator()
        self.ast = ast

    def _visit_exception(self, node):
        raise NoVisitMethodException(f"No visit_{type(node).__name__} method")

    def _visit(self, node: Union[NumAST, StringAST], is_negative):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        return visitor(node, is_negative)

    def _visit_BinOpAST(self, node: BinOpAST, is_negative):
        if node.op.tok_type == Token.DIV:
            n_left = self._visit(node.left, is_negative=False)
            n_right = self._visit(node.right, is_negative=False)
            neg = bool(sum((int(is_negative), int(n_left[1]), int(n_right[1]))) % 2)
            code = ""
            code += f"{n_left[0]}\n"
            code += f"push eax\n"
            code += f"{n_right[0]}\n"
            code += f"push eax\n"
            code += f"pop ebx\n"
            code += f"pop eax\n"
            if neg:
                code += "mov edx, 1\n"
                code += "neg edx\n"
            code += f"idiv ebx\n"

            return code, is_negative
        return ""

    def _visit_UnOpAST(self, node: UnOpAST, is_negative):
        if node.op.tok_type == Token.MINUS:
            # is_negative = not is_negative
            n_right = self._visit(node.right, is_negative=False)
            code = ""
            code += f"{n_right[0]}\n"
            # code += "pop eax\n"
            code += "neg eax\n"
            return code, True

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST], is_negative):
        code = ""
        code += f"mov eax, {node.value}"
        return code, is_negative

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def _visit_StringAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def interpret(self):
        self.code_generator.generated_code = self._visit(self.ast, False)[0]
        self.code_generator.write_to_file()
