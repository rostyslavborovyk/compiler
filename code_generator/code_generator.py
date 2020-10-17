from typing import Callable


class CodeGenerator:
    def __init__(self):
        self.label_unique_id = 0
        self.generated_code = []

    def add(self, code: str) -> None:
        self.generated_code.append(code)

    def _get_unique_id(self):
        self.label_unique_id += 1
        return self.label_unique_id

    def div_op(self, left: Callable, right: Callable) -> None:
        left()
        self.add(f"push eax")
        right()
        self.add("push eax")
        self.add("pop ebx")
        self.add("pop eax")
        self.add("cdq")
        self.add("idiv ebx")

    def mul_op(self, left: Callable, right: Callable) -> None:
        left()
        self.add("push eax")
        right()
        self.add("push eax")
        self.add("pop eax")
        self.add("pop ebx")
        self.add("cdq")
        self.add("imul ebx")

    def logical_or_op(self, left: Callable, right: Callable) -> None:
        l1 = f"_there_{self._get_unique_id()}"
        l2 = f"_end1_{self._get_unique_id()}"
        l3 = f"_end0_{self._get_unique_id()}"
        l4 = f"_end_{self._get_unique_id()}"

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
        with open("2-02-Python-IV-82-Borovyk.asm", "w") as f:
            f.write(generated_string)
