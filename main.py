from interpeter import Interpreter
from lexer import Lexer
from my_parser import Parser


# todo maybe add tests
def main():
    with open("1-02-Python-IV-82-Borovyk.txt", "rb") as f:
        text = str(f.read())[2:-1]  # trims b'str' to str

    # print(f"Text: {text}")
    lexer = Lexer(text)
    tokens = lexer.get_tokens()
    # print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
    interpreter = Interpreter(ast)
    interpreter.interpret()


if __name__ == '__main__':
    main()
