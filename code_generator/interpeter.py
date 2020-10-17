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

    def _visit_exception(self, node) -> None:
        raise NoVisitMethodException(f"No _visit_{type(node).__name__} method")

    def _visit(self, node: Type[AST]) -> None:
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        visitor(node)

    def _visit_StatementsListAST(self, node: StatementsListAST) -> None:
        for child in node.children:
            self._visit(child)

            # optional indent after each statement
            self.code_generator.add("\n")

    def _visit_AssignExpAST(self, node: AssignExpAST) -> None:
        var_id = node.var_id.value

        self._visit(node.exp)

        # assigning new variable
        if var_id not in self.var_map:
            self.code_generator.add("push eax")
            self._decrement_offset()
            self.var_map.update({var_id: self.var_offset})

        # assigning existing variable
        else:
            var_offset = self.var_map.get(var_id)
            self.code_generator.add(f"mov [ebp - {-var_offset}], eax")

    def _visit_IdAST(self, node: IdAST) -> None:
        var_offset = self.var_map.get(node.var_id)
        if var_offset is None:
            raise NoSuchVariableException(f"No such variable {node.var_id}")

        self.code_generator.add(f"mov eax, [ebp - {-var_offset}]")

    def _visit_BinOpAST(self, node: BinOpAST) -> None:
        if node.op.tok_type == Token.DIV:
            self.code_generator.div_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.tok_type == Token.MUL:
            self.code_generator.mul_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.tok_type == Token.BUILTIN_WORD and node.op.value == Token.BUILTIN_WORDS["or"]:
            self.code_generator.logical_or_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

    def _visit_UnOpAST(self, node: UnOpAST) -> None:
        if node.op.tok_type == Token.MINUS:
            self._visit(node.right)

            self.code_generator.add("neg eax")

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST]) -> None:
        self.code_generator.add(f"mov eax, {node.value}")

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def _visit_StringAST(self, node: Union[NumAST, StringAST]):
        print(f"visiting {node}")
        pass

    def interpret(self):
        self._visit(self.ast)
        self.code_generator.write_to_file()
