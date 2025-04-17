# compiler/lexical_analysis/scanner.py

from .file_reader import FileReader

class Scanner:
    def __init__(self, input_path: str):
        self.source = FileReader(input_path)
        self.line_ptr = 0
        self.scan_ptr = 0
        self.curr_line = self.source.get_line(0) if self.source.line_count() > 0 else ""
        self.exhausted = self.curr_line == ""
        self.returned_newline = False

    def unget_char(self):
        if self.returned_newline:
            self.returned_newline = False
        elif self.scan_ptr > 0:
            self.scan_ptr -= 1

    def get_char(self):
        if self.exhausted:
            return None

        if self.scan_ptr >= len(self.curr_line):
            if not self.returned_newline:
                self.returned_newline = True
                return '\n'
            else:
                self._next_line()
                if self.exhausted:
                    return None

        # Make sure scan_ptr is valid before indexing
        if self.scan_ptr < len(self.curr_line):
            char = self.curr_line[self.scan_ptr]
            self.scan_ptr += 1
            self.returned_newline = False
            print(f"[scanner - get_char] '{char}' @ line {self.line_ptr}, col {self.scan_ptr}")
            return char

        return None

    def _next_line(self):
        self.line_ptr += 1
        if self.line_ptr >= self.source.line_count():
            self.exhausted = True
            self.curr_line = ""
        else:
            self.curr_line = self.source.get_line(self.line_ptr)
            self.scan_ptr = 0
