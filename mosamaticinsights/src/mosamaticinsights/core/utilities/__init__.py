import sys
import pathlib


def home():
    return pathlib.Path.home()

def is_macos():
    return sys.platform.lower() == 'darwin'