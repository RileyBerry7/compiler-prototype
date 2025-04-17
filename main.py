# main.py
from compiler.compiler import Compiler

def main():
    print("hello world :3")

    my_compiler = Compiler()
    my_compiler.run_lexer()
    my_compiler.token_stream.display("output/token_stream.txt")

if __name__ == "__main__":
    main()