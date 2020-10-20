from typing import Callable
import re


class CodeGenerator:
    def __init__(self):
        self.label_unique_id = 0
        self.generated_code = []

    def add(self, code: str) -> None:
        self.generated_code.append(code)

    def _get_unique_id(self):
        self.label_unique_id += 1
        return self.label_unique_id

    def div_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add(f"push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop eax")
        # self.add("cdq")
        self.add("idiv ebx")

    def mul_op(self, left: Callable[[], None], right: Callable[[], None]) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop eax")
        self.add("pop ebx")
        self.add("cdq")
        self.add("imul ebx")

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

    def write_to_file(self):
        generated_string = "\n".join(self.generated_code)
        with open("3-02-Python-IV-82-Borovyk.asm", "w") as f:
            f.write(generated_string)

    def _double_offset(self, string: str) -> str:
        # doubling 4 byte offset to 8 bytes
        res = re.search(re.compile(r"mov ..., \[rbp - \d+]"), string)
        if res:
            res = res.group(0)
            d = re.search(re.compile(r"\d+"), res).group(0)
            d = str(2 * int(d))
            res = re.sub(re.compile(r"\d+"), d, res)
        return res if res else string

    def write_to_test_file(self, output_path):
        # adding prolog
        gc = [
            "xor rdx, rdx",
            "push rbp",
            "mov rbp, rsp",
        ]
        gc.extend(self.generated_code)
        self.generated_code = gc

        # replacing 32 bit registers with 64 bit (for 64 bit systems)
        self.generated_code = map(lambda x: x.replace("eax", "rax"), self.generated_code)
        self.generated_code = map(lambda x: x.replace("ebx", "rbx"), self.generated_code)
        self.generated_code = map(lambda x: x.replace("edx", "rdx"), self.generated_code)
        self.generated_code = map(lambda x: x.replace("ebp", "rbp"), self.generated_code)

        # doubling the offset from 4 bytes per var to 8 bytes (for 64 bit systems)
        self.generated_code = map(lambda x: self._double_offset(x), self.generated_code)

        # adding epilog
        self.generated_code = list(self.generated_code)
        self.generated_code.extend([
            "mov rsp, rbp",
            "pop rbp"
        ])

        generated_string = "\n\t".join(map(lambda x: f"\"{x};\"", self.generated_code))

        with open("build/build_template.cpp", "r") as f:
            template = f.read()

        template = template.replace("CODE", generated_string)

        path = output_path or "build/main.cpp"

        with open(path, "w") as f:
            f.write(template)
