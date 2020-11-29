from collections import namedtuple

from common.types import CycleLabels
from my_parser.AST import NumAST, StringAST, BinOpAST, UnOpAST, AST, StatementsListAST, AssignExpAST, IdAST, \
    CondStatementAST, \
    FunctionAST, FunctionCallAST, ProgramAST, WhileStatementAST, BreakStatementAST, ContinueStatementAST, \
    ReturnStatementAST, CompOpAST
from typing import Union, Type, Dict, List

from code_generator.code_generator import CodeGenerator
from exceptions.my_exceptions import NoVisitMethodException, NoSuchVariableException, InvalidSyntaxException
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

        # list of end_of_cycle labels for BREAK to exit
        self.cycle_labels_list: List[CycleLabels] = []

    def _decrement_offset(self) -> None:
        self.var_offset -= 4

    def _visit_exception(self, node) -> None:
        raise NoVisitMethodException(f"No _visit_{type(node).__name__} method")

    def _visit(self, node: Type[AST], **kwargs) -> None:
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._visit_exception)
        visitor(node, **kwargs)

    def _visit_ProgramAST(self, node: ProgramAST, **kwargs):
        # print("visited ProgramAst")
        for node in node.hl_statements:
            self._visit(node, **kwargs)

    def _visit_FunctionAST(self, node: FunctionAST, **kwargs):
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
        func_pre_end_label = f"{func_label}_pre_end"
        # adding labels to omit function
        self.code_generator.add(f"jmp {func_label}_end")
        self.code_generator.add(f"{func_label}:")
        self.code_generator.add("push ebp")
        self.code_generator.add("mov ebp, esp")

        for statement in node.statement_list.children:
            self._visit(statement, func_pre_end_label=func_pre_end_label)

        # pre end label for jumping after return statement
        self.code_generator.add(f"{func_pre_end_label}:")

        self.code_generator.add("mov esp, ebp")
        self.code_generator.add("pop ebp")

        self.code_generator.add(f"ret {len(node.func_args) * 4 if len(node.func_args) else ''}")
        self.code_generator.add(f"{func_label}_end:")
        # removing local vars from local var map
        self.func_args_var_map = dict()
        # restoring var map state and offset
        self.var_map = saved_var_map
        self.var_offset = saved_offset

    def _visit_FunctionCallAST(self, node: FunctionCallAST, **kwargs):
        # print("visited function call")
        if node.args:
            for arg in node.args[::-1]:
                if arg.tok_type in (Token.NUMBER_DECIMAL, Token.NUMBER_BINARY, Token.NUMBER_HEX):
                    self.code_generator.add(f"push {arg.value}")
                elif arg.tok_type == Token.ID:
                    self._visit(IdAST(arg.value), **kwargs)
                    self.code_generator.add(f"push eax")

        self.code_generator.add(f"call {self.code_generator.func_label_wrapper(node.func_id.value)}")

    def _visit_StatementsListAST(self, node: StatementsListAST, **kwargs) -> None:
        for child in node.children:
            self._visit(child, **kwargs)

            # optional indent after each statement
            # self.code_generator.add("\n")

    def _visit_AssignExpAST(self, node: AssignExpAST, **kwargs) -> None:
        var_id = node.var_id.value

        self._visit(node.exp, **kwargs)

        # assigning new variable
        if var_id not in self.var_map:
            self.code_generator.add("push eax")
            self._decrement_offset()
            self.var_map.update({var_id: self.var_offset})

        # assigning existing variable
        else:
            var_offset = self.var_map.get(var_id)
            self.code_generator.add(f"mov [ebp - {-var_offset}], eax")

    def _visit_IdAST(self, node: IdAST, **kwargs) -> None:
        var_offset = self.var_map.get(node.var_id)
        if var_offset is not None:
            self.code_generator.add(f"mov eax, [ebp - {-var_offset}]")
        else:
            var_offset = self.func_args_var_map.get(node.var_id)
            if var_offset is not None:
                self.code_generator.add(f"mov eax, [ebp + {var_offset}]")
        if var_offset is None:
            raise NoSuchVariableException(f"No such variable {node.var_id}")

    def _visit_CondStatementAST(self, node: CondStatementAST, **kwargs) -> None:
        self.code_generator.if_statement(
            lambda: self._visit(node.cond, **kwargs),
            lambda: self._visit(node.node_if, **kwargs),
            lambda: self._visit(node.node_else, **kwargs),
        )

    def _visit_WhileStatementAST(self, node: WhileStatementAST, **kwargs) -> None:
        self.code_generator.while_statement(
            lambda: self._visit(node.cond, **kwargs),
            lambda: self._visit(node.while_body, **kwargs),
            lambda x: self.cycle_labels_list.append(x)
        )
        if not len(self.cycle_labels_list):
            raise InvalidSyntaxException("No end_of_cycle label")

        self.cycle_labels_list.pop()

    def _visit_BreakStatementAST(self, node: BreakStatementAST, **kwargs) -> None:
        """
        Looks to last CycleLabels in self.cycle_labels_list, and set code to jump to CycleLabels.end,
        removes this label from list
        """
        if not len(self.cycle_labels_list):
            raise InvalidSyntaxException("Statement break should be used inside of a loop")

        self.code_generator.add(f"jmp {self.cycle_labels_list[-1].end}")

    def _visit_ContinueStatementAST(self, node: ContinueStatementAST, **kwargs) -> None:
        """
        Looks to last CycleLabels in self.cycle_labels_list, and set code to jump to CycleLabels.start,
        removes this label from list
        """
        if not len(self.cycle_labels_list):
            raise InvalidSyntaxException("Statement break should be used inside of a loop")

        self.code_generator.add(f"jmp {self.cycle_labels_list[-1].start}")

    def _visit_ReturnStatementAST(self, node: ReturnStatementAST, **kwargs) -> None:
        self._visit(node.exp)
        label = kwargs.get("func_pre_end_label", None)
        if label is not None:
            # print("Pre end label is ", label)
            self.code_generator.add(f"jmp {label}")

    def _visit_BinOpAST(self, node: BinOpAST, **kwargs) -> None:
        if node.op.value == Token.OPERATIONS["DIV"]:
            self.code_generator.div_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["MUL"]:
            self.code_generator.mul_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["MOD"]:
            self.code_generator.mod_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["PLUS"]:
            self.code_generator.plus_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["MINUS"]:
            self.code_generator.sub_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["OR"]:
            self.code_generator.logical_or_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

    def _visit_CompOpAST(self, node: CompOpAST, **kwargs) -> None:
        if node.op.value == Token.OPERATIONS["EQ"]:
            self.code_generator.eq_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["NEQ"]:
            self.code_generator.neq_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["GR"]:
            self.code_generator.gr_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["LS"]:
            self.code_generator.ls_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["GRE"]:
            self.code_generator.gre_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

        elif node.op.value == Token.OPERATIONS["LSE"]:
            self.code_generator.lse_op(
                lambda: self._visit(node.left, **kwargs),
                lambda: self._visit(node.right, **kwargs)
            )

    def _visit_UnOpAST(self, node: UnOpAST, **kwargs) -> None:
        if node.op.value == Token.OPERATIONS["MINUS"]:
            self._visit(node.right, **kwargs)

            self.code_generator.add("neg eax")

    def _visit_DecimalAST(self, node: Union[NumAST, StringAST], **kwargs) -> None:
        self.code_generator.add(f"mov eax, {node.value}")

    def _visit_BinaryAST(self, node: Union[NumAST, StringAST], **kwargs):
        print(f"visiting {node}")
        self.code_generator.add(f"mov eax, {node.value}")

    def _visit_HexAST(self, node: Union[NumAST, StringAST], **kwargs):
        print(f"visiting {node}")
        self.code_generator.add(f"mov eax, {node.value}")

    def _visit_StringAST(self, node: Union[NumAST, StringAST], **kwargs):
        print(f"visiting {node}")
        pass

    def interpret(self, output_path, test, system_arch):
        self._visit(self.ast)

        self.code_generator.write_to_asm_file(output_path, system_arch)

        self.code_generator.write_to_cpp_file(system_arch=system_arch, test=test)
