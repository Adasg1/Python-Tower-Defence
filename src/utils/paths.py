import sys
import os

def get_path(relative_path):
    if getattr(sys, 'frozen', False):
        # ścieżka do folderu tymczasowego (MEIPASS)
        base_path = sys._MEIPASS
    else:
        # ścieżka do katalogu projektu
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)