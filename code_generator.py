class CodeGenerator:
    def __init__(self):
        self.generated_code = ""

    def add_write_to_eax_from_var(self, var):
        self.generated_code += f"mov eax, {var}\n"

    def add_write_to_b_from_eax(self, is_str=False):
        if not is_str:
            self.generated_code += "mov b, eax\n"
        else:
            self.generated_code += "mov b, al\n"

    def write_to_file(self):
        with open("1-02-Python-IV-82-Borovyk.asm", "w") as f:
            f.write(self.generated_code)

