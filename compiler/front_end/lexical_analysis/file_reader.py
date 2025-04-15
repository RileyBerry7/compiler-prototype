# compiler/lexical_analysis/file_reader.py

import os

class FileReader:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[FileReader Error] File not found: {path}")
        try:
            with open(path, 'r') as f:
                self.lines = f.readlines()
        except OSError as e:
            raise IOError(f"[FileReader Error] Failed to read file: {e}")

    def get_line(self, index: int) -> str:
        return self.lines[index].rstrip('\n')

    def line_count(self) -> int:
        return len(self.lines)
