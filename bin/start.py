# coding:utf-8
import os
import sys

BASIC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASIC_PATH)

from core import scr

if __name__ == '__main__':
    scr.run()
