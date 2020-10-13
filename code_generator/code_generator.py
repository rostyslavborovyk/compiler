class CodeGenerator:
    def __init__(self):
        self.generated_code = ""

    def write_to_file(self):
        with open("2-02-Python-IV-82-Borovyk.asm", "w") as f:
            f.write(self.generated_code)
