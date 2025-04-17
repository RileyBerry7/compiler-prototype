# compiler/compiler.py

from .symbol_table import SymbolTable
from .error_table  import ErrorTable

from compiler.front_end.lexical_analysis.lexer import Lexer


class Compiler:
    def __init__(self, input_file_path:
                str="custom-cpp-compiler/input/test.cpp"):

        self.in_file = input_file_path
        self.symbols = SymbolTable()
        self.errors  = ErrorTable()

    def run_lexer(self):
        lexer = Lexer(self.symbols, self.errors)

        # Lexical analysis
        lexer.scan(self.in_file)
