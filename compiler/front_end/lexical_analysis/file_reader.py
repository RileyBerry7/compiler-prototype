import os

class FileReader:
    def __init__(self, path: str):
        print(f"[DEBUG] Attempting to open file: {os.path.abspath(path)}")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[FileReader Error] File not found: {path}")
        try:
            with open(path, 'r') as f:
                self.lines = f.readlines()
            print(f"[DEBUG] Read {len(self.lines)} lines from {path}")
        except OSError as e:
            raise IOError(f"[FileReader Error] Failed to read file: {e}")

    def get_line(self, index: int) -> str:
        if 0 <= index < len(self.lines):
            return self.lines[index].rstrip('\n')
        return ""

    def line_count(self) -> int:
        return len(self.lines)
