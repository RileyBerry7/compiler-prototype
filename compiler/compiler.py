# compiler/compiler.py

from .symbol_table import SymbolTable
from .error_table  import ErrorTable

from compiler.front_end.lexical_analysis.lexer import Lexer


def compiler():

    input_directory = "/input/test.cpp"
    symbols = SymbolTable()
    errors  = ErrorTable()
    lexer   = Lexer(symbols, errors)

    # Lexical analysis
    lexer.scan(input_directory)
