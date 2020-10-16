from my_parser.AST import NumAST, StringAST, BinOpAST, UnOpAST, AST, StatementsListAST
from typing import Union, Type

from code_generator.code_generator import CodeGenerator
from exceptions.my_exceptions import NoVisitMethodException
from lexer.my_token import Token


class Interpreter:
    def __init__(self, ast: Type[AST]):
        self.code_generator = CodeGenerator()
        self.ast = ast

    def _visit_exception(self, node, *args):
        raise NoVisitMethodException(f"No _visit_{type(node).__name__} method")

    def _visit(self, node: Type[AST], *args):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        return visitor(node, *args)

    def _visit_StatementsListAST(self, node: StatementsListAST, *args):
        node = self._visit(node.children[0], *args)
        return node

    def _visit_BinOpAST(self, node: BinOpAST, is_negative, top_level_op=False):
        if node.op.tok_type == Token.DIV:
            n_left = self._visit(node.left, False)
            self.code_generator.add(f"push eax")
            n_right = self._visit(node.right, False)
            self.code_generator.add(f"push eax")
            self.code_generator.add(f"pop ebx")
            self.code_generator.add(f"pop eax")

            neg = is_negative ^ n_left ^ n_right
            if neg and top_level_op:
                self.code_generator.add("mov edx, 1")
                self.code_generator.add("neg edx")
                self.code_generator.add("neg eax")
            self.code_generator.add(f"idiv ebx")
            return neg
        return ""

    def _visit_UnOpAST(self, node: UnOpAST, is_negative, top_level_op=False):
        if node.op.tok_type == Token.MINUS:
            is_negative = not is_negative
            n_right = self._visit(node.right, is_negative)

            if top_level_op and n_right:
                self.code_generator.add("neg eax")
            return n_right

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST], is_negative):
        self.code_generator.add(f"mov eax, {node.value}")

        return is_negative

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def _visit_StringAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def interpret(self):
        self._visit(self.ast, False, True)
        self.code_generator.write_to_file()
