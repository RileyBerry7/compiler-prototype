from compiler.symbol_table import SymbolTable
from compiler.error_table import ErrorTable
from .scanner import Scanner
from .file_writer import FileWriter
from compiler.front_end.lexical_analysis.tokens import *

class Lexer:
    def __init__(self, symbols: SymbolTable, errors: ErrorTable):
        self.ids = symbols
        self.errs = errors
        self.out_dir = "/token_stream.txt"

    def scan(self, in_path: str, out_path: str = None):
        scanner = Scanner(in_path)
        token_stream = TokenStream()
        lexeme = []
        line = 1
        column = 1

        ######################################################################################################
        # Main Loop - Scans all chars in order, from the infile
        while not scanner.exhausted:
            curr_char = scanner.get_char()

            # Redundancy - break loop early on Invalid char
            if curr_char is None:
                break

            # ===== Handle Newline =====
            if curr_char == '\n':
                line += 1
                column = 1
                continue

            # ===== Skip whitespace =====
            if curr_char.isspace():
                column += 1
                continue

            # ===== IDENTIFIERS / KEYWORDS =====
            if curr_char.isalpha() or curr_char == '_':
                lexeme.append(curr_char)
                start_col = column
                column += 1

                # Consume the rest of the identifier
                while True:
                    p = scanner.peak()
                    if p is not None and p != '\n' and (p.isalnum() or p == '_'):
                        c = scanner.get_char()
                        lexeme.append(c)
                        column += 1
                    else:
                        break

                # Assemble / Add Identifier token
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

                # Consume the rest of the number (handle float with one dot)
                while True:
                    p = scanner.peak()
                    if p is None or p == '\n':
                        break
                    if p.isdigit():
                        c = scanner.get_char()
                        lexeme.append(c)
                        column += 1
                        continue
                    if p == '.' and not is_float:
                        c = scanner.get_char()
                        is_float = True
                        lexeme.append(c)
                        column += 1
                        continue
                    # anything else ends the number
                    break

                # Assemble / Add NUMBER token
                token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL
                token_stream.add(Token(token_type, ''.join(lexeme), line, start_col))
                lexeme = []
                continue

            # ===== OPERATORS / PUNCTUATION / COMMENTS =====
            if curr_char in operators or curr_char in punctuations:

                start_col = column
                # build lookahead string up to 3 chars
                second_char = scanner.peak(0) or ''
                third_char = scanner.peak(1) or ''
                lookahead = curr_char + second_char + third_char

                # Reduce lookahead until it matches a token
                while len(lookahead) > 1 and lookahead not in token_dict:
                    lookahead = lookahead[:-1]

                # Check if COMMENT
                if token_dict.get(lookahead) == TokenType.COMMENT:
                    comment = [curr_char]
                    # consume the '//' prefix
                    for _ in range(len(lookahead) - 1):
                        comment.append(scanner.get_char())
                    # accumulate until newline or EOF
                    while True:
                        peak = scanner.peak(0)
                        if peak is None or peak == '\n':
                            break
                        c = scanner.get_char()
                        comment.append(c)
                    token_stream.add(Token(TokenType.COMMENT, ''.join(comment), line, start_col))
                    column = 1
                    line += 1
                    continue

                # Not a comment: emit the operator/punctuation
                token_stream.add(Token(token_dict.get(lookahead, TokenType.UNKNOWN), lookahead, line, start_col))
                column += len(lookahead)
                # consume the extra chars
                for _ in range(len(lookahead) - 1):
                    scanner.get_char()
                continue

            # ===== UNKNOWN CHAR =====
            token_stream.add(Token(TokenType.UNKNOWN, curr_char, line, column))
            column += 1

        # Debug output
        print("[DEBUG] Done scanning.")
        print(f"[DEBUG] Tokens in stream: {len(token_stream._TokenStream__stream)}")
        for tok in token_stream._TokenStream__stream:
            print(f"{tok.type.name} => {tok.lexeme}")
        return token_stream
