import os
import sys

GAME_ROOT = os.path.dirname(__file__)
CODE_PATH = os.path.join(GAME_ROOT, "code")

if CODE_PATH not in sys.path:
    sys.path.insert(0, CODE_PATH)

from game.main import main

if __name__ == "__main__":
    main()