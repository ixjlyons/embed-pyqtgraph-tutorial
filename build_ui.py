"""
Compiles PyQt UI templates found in SRC and places the corresponding compiled
Python modules in DEST. Output files have the same name, but have a `.py`
extension instead of `.ui`.
"""

import os
from PyQt4 import uic

SRC = '.'
DEST = '.'

if __name__ == '__main__':
    uic.compileUiDir(SRC, map=lambda src, name: (DEST, name))
