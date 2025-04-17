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
        token_stream = TokenStream()
        lexeme = []
        line = 1
        column = 1

        while not scanner.exhausted:
            curr_char = scanner.get_char()

            if curr_char is None:
                break

            if curr_char == '\n':
                line += 1
                column = 1
                continue

            if curr_char.isspace():
                column += 1
                continue

            # ===== IDENTIFIERS / KEYWORDS =====
            if curr_char.isalpha() or curr_char == '_':
                lexeme.append(curr_char)
                start_col = column
                column += 1

                while True:
                    c = scanner.get_char()
                    if c and (c.isalnum() or c == '_'):
                        lexeme.append(c)
                        column += 1
                    else:
                        if c:
                            scanner.unget_char()
                        break

                token_str = ''.join(lexeme)
                token_type = token_dict.get(token_str, TokenType.IDENTIFIER)
                token_stream.add(Token(token_type, token_str, line, start_col))
                lexeme = []
                continue

            # ===== NUMBERS =====
            if curr_char.isdigit():
                lexeme.append(curr_char)
                start_col = column
                column += 1
                is_float = False

                while True:
                    c = scanner.get_char()
                    if c and c.isdigit():
                        lexeme.append(c)
                        column += 1
                    elif c == '.' and not is_float:
                        is_float = True
                        lexeme.append(c)
                        column += 1
                    else:
                        if c:
                            scanner.unget_char()
                        break

                token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL
                token_stream.add(Token(token_type, ''.join(lexeme), line, start_col))
                lexeme = []
                continue

            # ===== OPERATORS & PUNCTUATION =====
            start_col = column

            second_char = scanner.get_char() or ''
            third_char = scanner.get_char() or ''

            lookahead = curr_char + second_char
            triple = lookahead + third_char

            if triple in token_dict:
                token_stream.add(Token(token_dict[triple], triple, line, start_col))
                column += 3
                continue
            else:
                scanner.unget_char()  # undo third
            if lookahead in token_dict:
                token_stream.add(Token(token_dict[lookahead], lookahead, line, start_col))
                column += 2
                continue
            else:
                scanner.unget_char()  # undo second
            if curr_char in token_dict:
                token_stream.add(Token(token_dict[curr_char], curr_char, line, start_col))
                column += 1
                continue

            # ===== UNKNOWN CHAR =====
            token_stream.add(Token(TokenType.UNKNOWN, curr_char, line, column))
            column += 1

        print("[DEBUG] Done scanning.")
        print(f"[DEBUG] Tokens in stream: {len(token_stream._TokenStream__stream)}")
        for tok in token_stream._TokenStream__stream:
            print(f"{tok.type.name} => {tok.lexeme}")
        return token_stream
