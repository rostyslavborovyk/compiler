class CodeGenerator:
    def __init__(self):
        self.generated_code = []

    def add(self, code: str) -> None:
        self.generated_code.append(code)

    def write_to_file(self):
        generated_string = "\n".join(self.generated_code)
        with open("2-02-Python-IV-82-Borovyk.asm", "w") as f:
            f.write(generated_string)
