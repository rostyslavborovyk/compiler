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
arg_parser.add_argument(
    "--arch",
    dest="arch",
    nargs="?",
    default=32,
    type=int,
    metavar="arch",
    help="architecture for assembler (32 or 64)",
)


def compile_to_exec(cpp_path, exec_path, arch):
    subprocess.run(f"g++ -m{arch} -masm=intel {cpp_path} -o {exec_path}".split(" "))
    # p = subprocess.Popen([f"./{exec_path}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE)
    # output, err = p.communicate()
    # res = output.decode("utf-8")
    # res = res.replace("\n", "")
    # print(res)


def compiler(text, arch, output_asm=None, test=False, output_cpp=None, output_exec=None):
    lexer = Lexer(text)
    tokens = lexer.get_tokens()
    # pprint(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    # ast.prettyAST()
    interpreter = Interpreter(ast)
    interpreter.interpret(output_asm, test, arch)
    compile_to_exec(output_cpp, output_exec, arch)


def main():
    args = arg_parser.parse_args()
    src = args.src.name
    if src[-3:] != ".py":
        raise ValueError("--src file should have .py extension")

    asm_out = args.asm_out.name
    if asm_out[-4:] != ".asm":
        raise ValueError("--output file should have .asm extension")

    arch = args.arch

    cpp_out = "output.cpp"
    output_exec = "output"

    with open(src, "rb") as f:
        program_text = str(f.read())[2:-1]  # trims b"str" to str

    compiler(
        program_text,
        output_asm=asm_out,
        output_cpp=cpp_out,
        output_exec=output_exec,
        arch=arch
    )


if __name__ == "__main__":
    main()
