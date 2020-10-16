from my_parser.AST import NumAST, StringAST, BinOpAST, UnOpAST, AST, StatementsListAST, AssignExpAST, IdAST
from typing import Union, Type, Dict

from code_generator.code_generator import CodeGenerator
from exceptions.my_exceptions import NoVisitMethodException, NoSuchVariableException
from lexer.my_token import Token


class Interpreter:
    def __init__(self, ast: Type[AST]):
        self.code_generator = CodeGenerator()
        self.ast = ast

        # var_id: offset
        self.var_map: Dict[str, int] = dict()
        self.var_offset = 0

    def _decrement_offset(self) -> None:
        self.var_offset -= 4

    def _visit_exception(self, node, *args):
        raise NoVisitMethodException(f"No _visit_{type(node).__name__} method")

    def _visit(self, node: Type[AST], *args):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        return visitor(node, *args)

    def _visit_StatementsListAST(self, node: StatementsListAST, *args):
        for child in node.children:
            self._visit(child, *args)
            # optional indent after each statement
            self.code_generator.add("\n")
        return node

    def _visit_AssignExpAST(self, node: AssignExpAST, is_negative, top_level_op=False):
        var_id = node.var_id.value

        self._visit(node.exp, is_negative, top_level_op)

        # assigning new variable
        if var_id not in self.var_map:
            self.code_generator.add("push eax")
            self._decrement_offset()
            self.var_map.update({var_id: self.var_offset})

        # assigning existing variable
        else:
            var_offset = self.var_map.get(var_id)
            self.code_generator.add(f"mov [ebp - {-var_offset}], eax")

    def _visit_IdAST(self, node: IdAST, is_negative, top_level_op=False):
        var_offset = self.var_map.get(node.var_id)
        if var_offset is None:
            raise NoSuchVariableException(f"No such variable {node.var_id}")

        self.code_generator.add(f"mov eax, [ebp - {-var_offset}]")
        return is_negative

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

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST], is_negative, top_level_op=False):
        self.code_generator.add(f"mov eax, {node.value}")
        if top_level_op and is_negative:
            self.code_generator.add("neg eax")
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
