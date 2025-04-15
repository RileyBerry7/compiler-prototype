# compiler/lexical_analysis/file_writer.py

import os

class FileWriter:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def write_line(self, line: str):
        try:
            with open(self.path, 'a') as f:
                f.write(line + '\n')
        except OSError as e:
            print(f"[FileWriter Error] Failed to write line: {e}")

    def overwrite(self, lines: list[str]):
        try:
            with open(self.path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
        except OSError as e:
            print(f"[FileWriter Error] Failed to overwrite file: {e}")
