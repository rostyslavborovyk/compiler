from AST import AST, NumAST, StringAST
from typing import Union

from code_generator import CodeGenerator
from my_exceptions import NoVisitMethodException


class Interpreter:
    def __init__(self, ast: Union[NumAST, StringAST]):
        self.code_generator = CodeGenerator()
        self.ast = ast

    def generic_visit(self, node):
        raise NoVisitMethodException(f"No visit_{type(node).__name__} method")

    def _visit(self, node: Union[NumAST, StringAST]):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST]):
        # print(f"visiting {node}")
        self.code_generator.add_write_to_eax_from_var(node.value)
        self.code_generator.add_write_to_b_from_eax()

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST]):
        # print(f"visiting {node}")
        value = node.value[2:]
        value += "b"
        self.code_generator.add_write_to_eax_from_var(value)
        self.code_generator.add_write_to_b_from_eax()

    def _visit_StringAST(self, node: Union[NumAST, StringAST]):
        # print(f"visiting {node}")
        value = node.value

        value = "\'" + value[1:-1] + "\'"
        self.code_generator.add_write_to_eax_from_var(value)
        self.code_generator.add_write_to_b_from_eax(is_str=True)

    def interpret(self):
        self._visit(self.ast)
        self.code_generator.write_to_file()
