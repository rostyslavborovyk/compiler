from AST import AST, NumAST, StringAST, BinOpAST, UnOpAST, DecimalAST
from typing import Union

from code_generator import CodeGenerator
from my_exceptions import NoVisitMethodException
from my_token import Token


class Interpreter:
    def __init__(self, ast: Union[NumAST, StringAST]):
        self.code_generator = CodeGenerator()
        self.ast = ast

    def visit_exception(self, node):
        raise NoVisitMethodException(f"No visit_{type(node).__name__} method")

    def _visit(self, node: Union[NumAST, StringAST]):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.visit_exception)
        return visitor(node)

    def _visit_BinOpAST(self, node: BinOpAST):
        if node.op.tok_type == Token.DIV:
            code = ""
            code += f"{self._visit(node.left)}\n"
            code += f"push eax\n"
            code += f"{self._visit(node.right)}\n"
            code += f"push eax\n"
            code += f"pop ebx\n"
            code += f"pop eax\n"
            code += f"idiv ebx\n"

            return code
        return ""

    def _visit_UnOpAST(self, node: UnOpAST):
        # todo process type of un_op
        code = ""
        code += f"{self._visit(node.right)}\n"
        # code += "pop eax\n"
        code += "neg eax\n"
        return code

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST]):
        code = ""
        code += f"mov eax, {node.value}"
        return code

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def _visit_StringAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def interpret(self):
        self.code_generator.generated_code = self._visit(self.ast)
        self.code_generator.write_to_file()
