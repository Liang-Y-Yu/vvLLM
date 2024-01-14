import os
import sys

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gen import main
from src.utils import gpt_fire


def entry_main():
    gpt_fire(main)


if __name__ == "__main__":
    entry_main()
