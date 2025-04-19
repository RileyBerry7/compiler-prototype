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

        line = 1
        column = 1
        indent_stack = [0]
        at_line_start = True

        while not scanner.exhausted:
            # Handle indentation at start of a new line
            if at_line_start:
                # Count leading spaces/tabs
                indent_count = 0
                while True:
                    p = scanner.peek()
                    if p == ' ':
                        scanner.get_char()
                        indent_count += 1
                        column += 1
                    elif p == '\t':
                        scanner.get_char()
                        indent_count += 4  # treat tab as width 4
                        column += 1
                    else:
                        break
                # Emit INDENT/DEDENT tokens
                prev_indent = indent_stack[-1]
                if indent_count > prev_indent:
                    indent_stack.append(indent_count)
                    token_stream.add(Token(TokenType.INDENT, '', line, column))
                while indent_count < indent_stack[-1]:
                    indent_stack.pop()
                    token_stream.add(Token(TokenType.DEDENT, '', line, column))
                at_line_start = False

            curr_char = scanner.get_char()
            if curr_char is None:
                break

            # ===== Handle Newline & END_OF_LINE =====
            if curr_char == '\n':
                token_stream.add(Token(TokenType.END_OF_LINE, '', line, column))
                line += 1
                column = 1
                at_line_start = True
                continue

            # ===== Skip other whitespace =====
            if curr_char.isspace():
                column += 1
                continue

            # ===== Block Comments (/* ... */) =====
            if curr_char == '/' and scanner.peek() == '*':
                start_col = column
                lexeme = [curr_char]
                scanner.get_char()
                lexeme.append('*')
                column += 2
                while True:
                    c = scanner.get_char()
                    if c is None:
                        self.errs.add_error("Unterminated block comment", line, column)
                        break
                    lexeme.append(c)
                    if c == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    if c == '*' and scanner.peek() == '/':
                        lexeme.append(scanner.get_char())
                        column += 1
                        break
                token_stream.add(Token(TokenType.COMMENT, ''.join(lexeme), line, start_col))
                continue

            # ===== Line Comments (// ...) =====
            if curr_char == '/' and scanner.peek() == '/':
                start_col = column
                lexeme = [curr_char]
                scanner.get_char()
                lexeme.append('/')
                column += 2
                while True:
                    p = scanner.peek()
                    if p is None or p == '\n':
                        break
                    c = scanner.get_char()
                    lexeme.append(c)
                    column += 1
                token_stream.add(Token(TokenType.COMMENT, ''.join(lexeme), line, start_col))
                continue

            # ===== Raw String Literals R"delim(... )delim" =====
            if curr_char == 'R' and scanner.peek() == '"':
                start_col = column
                lexeme = ['R']
                c = scanner.get_char()
                lexeme.append(c)  # consume '"'
                column += 1
                # read the delimiter until '('
                delim = []
                while True:
                    c = scanner.get_char()
                    if c is None:
                        self.errs.add_error("Unterminated raw string", line, column)
                        break
                    lexeme.append(c)
                    column += 1
                    if c == '(':
                        break
                    delim.append(c)
                closing = ')' + ''.join(delim) + '"'
                buffer = ''
                while True:
                    c = scanner.get_char()
                    if c is None:
                        self.errs.add_error("Unterminated raw string", line, column)
                        break
                    lexeme.append(c)
                    column += 1
                    buffer += c
                    if buffer.endswith(closing):
                        break
                    if c == '\n':
                        line += 1
                        column = 1
                token_stream.add(Token(TokenType.STRING_LITERAL, ''.join(lexeme), line, start_col))
                continue

            # ===== String Literals "..." =====
            if curr_char == '"':
                start_col = column
                lexeme = [curr_char]
                column += 1
                while True:
                    c = scanner.get_char()
                    if c is None or c == '\n':
                        self.errs.add_error("Unterminated string literal", line, column)
                        break
                    lexeme.append(c)
                    column += 1
                    if c == '\\':
                        nxt = scanner.get_char()
                        if nxt is None:
                            self.errs.add_error("Invalid escape sequence", line, column)
                            break
                        lexeme.append(nxt)
                        column += 1
                        continue
                    if c == '"':
                        break
                token_stream.add(Token(TokenType.STRING_LITERAL, ''.join(lexeme), line, start_col))
                continue

            # ===== Character Literals '...'<char> =====
            if curr_char == "'":
                start_col = column
                lexeme = [curr_char]
                column += 1
                c = scanner.get_char()
                if c is None or c == '\n':
                    self.errs.add_error("Unterminated char literal", line, column)
                else:
                    lexeme.append(c)
                    column += 1
                    if c == '\\':  # escape in char literal
                        nxt = scanner.get_char()
                        if nxt:
                            lexeme.append(nxt)
                            column += 1
                    c2 = scanner.get_char()
                    if c2 is None:
                        self.errs.add_error("Unterminated char literal", line, column)
                    else:
                        lexeme.append(c2)
                        column += 1
                        if c2 != "'":
                            self.errs.add_error("Invalid char literal", line, column)
                token_stream.add(Token(TokenType.CHAR_LITERAL, ''.join(lexeme), line, start_col))
                continue

            # ===== Identifiers / Keywords =====
            if curr_char.isalpha() or curr_char == '_':
                start_col = column
                lexeme = [curr_char]
                column += 1
                while True:
                    p = scanner.peek()
                    if p is not None and (p.isalnum() or p == '_'):
                        c = scanner.get_char()
                        lexeme.append(c)
                        column += 1
                    else:
                        break
                token_str = ''.join(lexeme)
                token_type = token_dict.get(token_str, TokenType.IDENTIFIER)
                token_stream.add(Token(token_type, token_str, line, start_col))
                continue

            # ===== Numbers (int & float) =====
            if curr_char.isdigit():
                start_col = column
                lexeme = [curr_char]
                column += 1
                is_float = False
                while True:
                    p = scanner.peek()
                    if p is None or p == '\n':
                        break
                    if p.isdigit():
                        c = scanner.get_char()
                        lexeme.append(c)
                        column += 1
                        continue
                    if p == '.' and not is_float:
                        c = scanner.get_char()
                        lexeme.append(c)
                        is_float = True
                        column += 1
                        continue
                    break
                token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL
                token_stream.add(Token(token_type, ''.join(lexeme), line, start_col))
                continue

            # ===== Operators / Punctuation =====
            if curr_char in operators or curr_char in punctuations:
                start_col = column
                # lookahead up to 3 chars
                lookahead = curr_char
                for i in range(2):
                    p = scanner.peek(i)
                    lookahead += p or ''
                # reduce until match
                while len(lookahead) > 1 and lookahead not in token_dict:
                    lookahead = lookahead[:-1]
                tok_type = token_dict.get(lookahead, TokenType.UNKNOWN)
                token_stream.add(Token(tok_type, lookahead, line, start_col))
                # consume extras
                for _ in range(len(lookahead) - 1):
                    scanner.get_char()
                column += len(lookahead)
                continue

            # ===== Unknown Character =====
            token_stream.add(Token(TokenType.UNKNOWN, curr_char, line, column))
            column += 1

        # After EOF, unwind remaining indents
        while len(indent_stack) > 1:
            indent_stack.pop()
            token_stream.add(Token(TokenType.DEDENT, '', line, column))

        return token_stream
