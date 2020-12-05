import copy
from typing import Callable, List
import re

from common.types import CycleLabels
from my_parser.AST import FunctionAST


class CodeGenerator:
    def __init__(self):
        self.label_unique_id = 0
        self.generated_code = []

    def add(self, code: str) -> None:
        self.generated_code.append(code)

    def _get_unique_id(self):
        self.label_unique_id += 1
        return self.label_unique_id

    def func_label_wrapper(self, func_id: str) -> str:
        return f"_func_{func_id}"

    def if_statement(self, cond: Callable[[], None], if_exp: Callable[[], None], else_exp: Callable[[], None]):
        unique_id = self._get_unique_id()

        l1 = f"_else_{unique_id}"
        l2 = f"_post_cond_{unique_id}"

        cond()
        self.add("cmp eax, 0")
        self.add(f"je {l1}")
        if_exp()
        self.add(f"jmp {l2}")
        self.add(f"{l1}:")
        else_exp()
        self.add(f"{l2}:")

    def while_statement(self, cond: Callable[[], None], while_body: Callable[[], None],
                        add_cycle_labels: Callable[[CycleLabels], None]) -> None:
        unique_id = self._get_unique_id()

        start_l = f"_start_cycle_{unique_id}"
        end_l = f"_end_cycle_{unique_id}"

        # adding CycleLabels for BREAK and CONTINUE statements
        add_cycle_labels(CycleLabels(start_l, end_l))

        self.add(f"{start_l}:")
        cond()
        self.add(f"cmp eax, 0")
        self.add(f"je {end_l}")
        while_body()
        self.add(f"jmp {start_l}")
        self.add(f"{end_l}:")

    def div_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add(f"push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop eax")
        self.add("cdq")
        self.add("idiv ebx")

    def mul_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop eax")
        self.add("pop ebx")
        self.add(f"xor edx, edx")
        self.add("cdq")
        self.add("imul ebx")

    def mod_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add(f"push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop eax")
        self.add("cdq")
        self.add("idiv ebx")
        self.add("mov eax, edx")

    def plus_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop eax")
        self.add("pop ebx")
        self.add("add eax, ebx")

    def sub_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop eax")
        self.add("sub eax, ebx")

    def eq_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("sete al")

    def neq_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("setne al")

    def gr_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("setg al")

    def ls_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("setl al")

    def gre_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("setge al")

    def lse_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop ecx")
        self.add("xor eax, eax")
        self.add("cmp ecx, ebx")
        self.add("setle al")

    def logical_or_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        unique_id = self._get_unique_id()

        l1 = f"_there_{unique_id}"
        l2 = f"_end1_{unique_id}"
        l3 = f"_end0_{unique_id}"
        l4 = f"_end_{unique_id}"

        left()
        self.add("cmp eax, 0")
        self.add(f"je {l1}")
        self.add(f"jmp {l2}")

        self.add(f"{l1}:")
        right()
        self.add("cmp eax, 0")
        self.add(f"je {l3}")
        self.add(f"jmp {l2}")

        self.add(f"{l2}:")
        self.add("mov eax, 1")
        self.add(f"jmp {l4}")

        self.add(f"{l3}:")
        self.add("xor eax, eax")
        self.add(f"jmp {l4}")

        self.add(f"{l4}:")

    def _convert_generated_code_to_64_arch(self) -> List:
        gen_code = copy.deepcopy(self.generated_code)

        # replacing 32 bit registers with 64 bit (for 64 bit systems)
        gen_code = map(lambda x: x.replace("eax", "rax"), gen_code)
        gen_code = map(lambda x: x.replace("ebx", "rbx"), gen_code)
        gen_code = map(lambda x: x.replace("ecx", "rcx"), gen_code)
        gen_code = map(lambda x: x.replace("edx", "rdx"), gen_code)
        gen_code = map(lambda x: x.replace("ebp", "rbp"), gen_code)
        gen_code = map(lambda x: x.replace("esp", "rsp"), gen_code)
        gen_code = map(lambda x: x.replace("cdq", "cqo"), gen_code)

        # doubling the offset from 4 bytes per var to 8 bytes (for 64 bit systems)
        gen_code = map(lambda x: self._double_offset(x), gen_code)
        gen_code = map(lambda x: self._double_outer_scope_offset(x), gen_code)
        gen_code = map(lambda x: self._double_ret(x), gen_code)
        gen_code = list(gen_code)
        return gen_code

    def _double_offset(self, string: str) -> str:
        # doubling 4 byte offset to 8 bytes
        res = re.search(re.compile(r".*\[rbp - \d+].*"), string)
        if res:
            res = res.group(0)
            d = re.search(re.compile(r"\d+"), res).group(0)
            d = str(2 * int(d))
            res = re.sub(re.compile(r"\d+"), d, res)
        return res if res else string

    def _double_outer_scope_offset(self, string: str) -> str:
        res = re.search(re.compile(r".*\[rbp \+ \d+].*"), string)
        if res:
            res = res.group(0)
            d = re.search(re.compile(r"\d+"), res).group(0)
            d = str(2 * int(d))
            res = re.sub(re.compile(r"\d+"), d, res)
        return res if res else string

    def _double_ret(self, string: str) -> str:
        res = re.search(re.compile(r"ret \d+"), string)
        if res:
            res = res.group(0)
            d = re.search(re.compile(r"\d+"), res).group(0)
            d = str(2 * int(d))
            res = re.sub(re.compile(r"\d+"), d, res)
        return res if res else string

    def write_to_asm_file(self, path, system_arch):
        gen_code = self.generated_code
        if system_arch == 64:
            gen_code = self._convert_generated_code_to_64_arch()
        generated_string = "\n".join(gen_code)
        with open(path, "w") as f:
            f.write(generated_string)

    def write_to_cpp_file(self, output_path=None, system_arch=32, test=False):
        gen_code = self.generated_code
        if system_arch == 64:
            gen_code = self._convert_generated_code_to_64_arch()

        generated_string = "\n\t".join(map(lambda x: f"\"{x};\"", gen_code))

        with open("build/build_template.cpp", "r") as f:
            template = f.read()

        template = template.replace("CODE", generated_string)

        if test:
            path = output_path or "build/main.cpp"

        else:
            path = output_path or "output.cpp"

        with open(path, "w") as f:
            f.write(template)
