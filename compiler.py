import argparse
import subprocess

from code_generator.interpeter import Interpreter
from lexer.lexer import Lexer
from my_parser.my_parser import Parser
from pprint import pprint

__all__ = ["compiler"]

arg_parser = argparse.ArgumentParser(description="Compiles python code to assembler")
arg_parser.add_argument(
    "--src",
    dest="src",
    nargs="?",
    type=argparse.FileType("r", encoding="utf-8"),
    metavar="src",
    help="path of src file with .py extension",
    required=True
)
arg_parser.add_argument(
    "--asm-out",
    dest="asm_out",
    nargs="?",
    default="output.asm",
    type=argparse.FileType("w", encoding="utf-8"),
    metavar="output",
    help="path of output file with .asm extension",
)


def compile_to_exec(cpp_path, exec_path):
    subprocess.run(f"g++ -masm=intel {cpp_path} -o {exec_path}".split(" "))
    # p = subprocess.Popen([f"./{exec_path}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE)
    # output, err = p.communicate()
    # res = output.decode("utf-8")
    # res = res.replace("\n", "")
    # print(res)


def compiler(text, system_arch, output_path=None, test=False):
    lexer = Lexer(text)
    tokens = lexer.get_tokens()
    # pprint(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    # ast.prettyAST()
    interpreter = Interpreter(ast)
    interpreter.interpret(output_path, test, system_arch)
    compile_to_exec("output.cpp", "output.exe")


def main():
    args = arg_parser.parse_args()
    src = args.src.name
    if src[-3:] != ".py":
        raise ValueError("--src file should have .py extension")
    asm_out = args.asm_out.name
    if asm_out[-4:] != ".asm":
        raise ValueError("--output file should have .asm extension")

    with open(src, "rb") as f:
        program_text = str(f.read())[2:-1]  # trims b"str" to str
    compiler(program_text, output_path=asm_out, system_arch=32)


if __name__ == "__main__":
    main()
