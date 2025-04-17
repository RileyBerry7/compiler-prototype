from string import punctuation

from compiler.symbol_table import SymbolTable
from compiler.error_table import ErrorTable
from .scanner import Scanner
from .file_writer import FileWriter

from compiler.front_end.lexical_analysis.tokens import *

###############################################################

# Input : Input Stream (raw code)
# Output: Token Stream + symbol table/error table population

class Lexer:
    def __init__(self, symbols: SymbolTable, errors: ErrorTable):
        self.ids  = symbols
        self.errs = errors
        self.out_dir  = "/token_stream.txt"

    def scan(self, in_path: str, out_path: str = None):

        scanner = Scanner(in_path)

        if not out_path:
            out_file = FileWriter(self.out_dir)
        else:
            out_file = FileWriter(out_path)

        ########################################
        # Initialize
        lexeme = []
        token_stream = TokenStream()
        line = 1
        column = 1

        while not scanner.exhausted:
            curr_char = scanner.get_char()

            if curr_char == '\n':
                line += 1
                column = 1
                continue
            elif curr_char.isspace():
                column += 1
                continue

            # Numbers
            if curr_char.isdigit():
                lexeme.append(curr_char)
                buffer_type = TokenType("INT_LITERAL")
                column_start = column
                column += 1

                while True:
                    curr_char = scanner.get_char()
                    if curr_char == '.':
                        buffer_type = TokenType("FLOAT_LITERAL")
                        lexeme.append(curr_char)
                        column += 1
                    elif curr_char.isdigit():
                        lexeme.append(curr_char)
                        column += 1
                    else:
                        scanner.unget_char()
                        break

                buffer_token = Token(buffer_type, ''.join(lexeme), line, column_start)
                token_stream.add(buffer_token)
                lexeme = []
                continue

            # Punctuation
            if curr_char in punctuation:
                buffer_type = token_dict[curr_char]
                buffer_token = Token(buffer_type, curr_char, line, column)
                token_stream.add(buffer_token)
                column += 1
                continue

            # Identifiers / Keywords
            if curr_char == '_' or curr_char.isalpha():
                lexeme.append(curr_char)
                column_start = column
                column += 1

                while True:
                    curr_char = scanner.get_char()
                    if curr_char.isalnum() or curr_char == '_':
                        lexeme.append(curr_char)
                        column += 1
                    else:
                        scanner.unget_char()
                        break

                joined = ''.join(lexeme)
                if joined in keywords:
                    buffer_type = token_dict[joined]
                else:
                    buffer_type = TokenType("IDENTIFIER")

                buffer_token = Token(buffer_type, joined, line, column_start)
                token_stream.add(buffer_token)
                lexeme = []
                continue

        return token_stream
