from code_generator.interpeter import Interpreter
from lexer.lexer import Lexer
from my_parser.my_parser import Parser
from pprint import pprint


def main(text, output_path=None, test=False):
    # print(f"Text: {bytes(text, encoding='utf-8')}")
    lexer = Lexer(text)
    tokens = lexer.get_tokens()
    # pprint(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    # ast.prettyAST()
    interpreter = Interpreter(ast)
    interpreter.interpret(output_path, test)


if __name__ == '__main__':
    with open("3-02-Python-IV-82-Borovyk.txt", "rb") as f:
        program_text = str(f.read())[2:-1]  # trims b'str' to str
    main(program_text)
