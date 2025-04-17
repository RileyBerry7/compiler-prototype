# compiler/compiler.py

from .symbol_table import SymbolTable
from .error_table  import ErrorTable

from compiler.front_end.lexical_analysis.lexer import Lexer
from compiler.front_end.lexical_analysis.tokens import *


class Compiler:
    def __init__(self, input_file_path:
                str="input/test.cpp"):

        self.in_file = input_file_path
        self.symbols = SymbolTable()
        self.errors  = ErrorTable()
        self.token_stream = TokenStream()

    def run_lexer(self):
        lexer = Lexer(self.symbols, self.errors)

        # Lexical analysis
        print("break-point 1")
        self.token_stream = lexer.scan(self.in_file)
