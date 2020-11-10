from my_parser.AST import NumAST, StringAST, BinOpAST, UnOpAST, AST, StatementsListAST, AssignExpAST, IdAST, CondExpAST, \
    FunctionAST, FunctionCallAST, ProgramAST
from typing import Union, Type, Dict

from code_generator.code_generator import CodeGenerator
from exceptions.my_exceptions import NoVisitMethodException, NoSuchVariableException
from lexer.my_token import Token
from copy import deepcopy


class Interpreter:
    def __init__(self, ast: ProgramAST):
        self.code_generator = CodeGenerator()
        self.ast = ast

        # var_id: offset
        self.var_map: Dict[str, int] = dict()
        self.func_args_var_map: Dict[str, int] = dict()
        self.func_map = set()
        self.var_offset = 0

    def _decrement_offset(self) -> None:
        self.var_offset -= 4

    def _visit_exception(self, node) -> None:
        raise NoVisitMethodException(f"No _visit_{type(node).__name__} method")

    def _visit(self, node: Type[AST]) -> None:
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        visitor(node)

    def _visit_ProgramAST(self, node: ProgramAST):
        # print("visited ProgramAst")
        for node in node.hl_statements:
            self._visit(node)

    def _visit_FunctionAST(self, node: FunctionAST):
        # print("visited function definition")
        # saving var map state and offset
        saved_var_map = deepcopy(self.var_map)
        saved_offset = self.var_offset
        # adding local vars to local var map
        for i in range(len(node.func_args)):
            var_id = node.func_args[i].value
            var_offset = 4 + (i + 1) * 4
            self.func_args_var_map.update({var_id: var_offset})

        func_label = f"{self.code_generator.func_label_wrapper(node.func_id.value)}"
        # adding labels to omit function
        self.code_generator.add(f"jmp {func_label}_end")
        self.code_generator.add(f"{func_label}:")
        self.code_generator.add("push ebp")
        self.code_generator.add("mov ebp, esp")

        for statement in node.statement_list.children:
            self._visit(statement)

        self.code_generator.add("mov esp, ebp")
        self.code_generator.add("pop ebp")
        self.code_generator.add(f"ret {len(node.func_args) * 4 if len(node.func_args) else ''}")
        self.code_generator.add(f"{func_label}_end:")
        # removing local vars from local var map
        self.func_args_var_map = dict()
        # restoring var map state and offset
        self.var_map = saved_var_map
        self.var_offset = saved_offset

    def _visit_FunctionCallAST(self, node: FunctionCallAST):
        print("visited function call")
        if node.args:
            for arg in node.args[::-1]:
                if arg.tok_type == Token.NUMBER_DECIMAL:
                    self.code_generator.add(f"push {arg.value}")
                elif arg.tok_type == Token.ID:
                    self._visit(IdAST(arg.value))
                    self.code_generator.add(f"push eax")

        self.code_generator.add(f"call {self.code_generator.func_label_wrapper(node.func_id.value)}")

    def _visit_StatementsListAST(self, node: StatementsListAST) -> None:
        for child in node.children:
            self._visit(child)

            # optional indent after each statement
            # self.code_generator.add("\n")

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
        if var_offset is not None:
            self.code_generator.add(f"mov eax, [ebp - {-var_offset}]")
        else:
            var_offset = self.func_args_var_map.get(node.var_id)
            if var_offset is not None:
                self.code_generator.add(f"mov eax, [ebp + {var_offset}]")
        if var_offset is None:
            raise NoSuchVariableException(f"No such variable {node.var_id}")

    def _visit_CondExpAST(self, node: CondExpAST) -> None:
        self.code_generator.if_statement(
            lambda: self._visit(node.cond),
            lambda: self._visit(node.node_if),
            lambda: self._visit(node.node_else),
        )

    def _visit_BinOpAST(self, node: BinOpAST) -> None:
        if node.op.value == Token.OPERATIONS["DIV"]:
            self.code_generator.div_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.value == Token.OPERATIONS["MUL"]:
            self.code_generator.mul_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.value == Token.OPERATIONS["PLUS"]:
            self.code_generator.plus_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.value == Token.OPERATIONS["MINUS"]:
            self.code_generator.sub_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

        elif node.op.value == Token.OPERATIONS["OR"]:
            self.code_generator.logical_or_op(
                lambda: self._visit(node.left),
                lambda: self._visit(node.right)
            )

    def _visit_UnOpAST(self, node: UnOpAST) -> None:
        if node.op.value == Token.OPERATIONS["MINUS"]:
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

    def interpret(self, output_path, test):
        self._visit(self.ast)
        if not test:
            self.code_generator.write_to_file()
        self.code_generator.write_to_test_file(output_path)
