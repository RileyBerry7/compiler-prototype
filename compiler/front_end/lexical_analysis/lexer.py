# lexer.py

from compiler.symbol_table import SymbolTable
from compiler.error_table import ErrorTable
from scanner import Scanner
from file_writer import FileWriter

###############################################################

accept_states    = {
                        0: 'id'
                        23,
                        12: 'num',
                        13: ''
                        15: 'comment',
                        28: 'operator'
                        31: 'int'
}
transition_table = {}

###############################################################

# Input : Input Stream (raw code)
# Output: Token Stream + symbol table/error table population

class Lexer:
    def __init__(self, symbols: SymbolTable, errors: ErrorTable):
        self.ids  = symbols
        self.errs = errors
        self.out_dir  = "/token_stream.txt"

    def scan(self, in_path: str, out_path: str=None):

        scanner = Scanner(in_path)

        if not out_path:
            out_file  = FileWriter(self.out_dir)
        else:
            out_file = FileWriter(out_path)

        token_stream = []

        # DFA usage
        lexeme = []
        while not scanner.exhausted:
            curr_char = scanner.get_char()

            if curr_char == ' ' or '\n':
                if lexeme:
                    # Execute state
                    is_valid = accept_states.get(state)
                    if is_valid is not None:
                        token_stream.append(is_valid)
                    # Else Error State
                    else:
                        self.errs.errors.append(lexeme)
                    state = 0
                    lexeme = []

                if curr_char == '\n':
                    if token_stream:
                        out_file.write_line("".join(token_stream))
                        token_stream = []

            else:
                lexeme.append(curr_char)
                state = transition_table[curr_char]

###############################################################

