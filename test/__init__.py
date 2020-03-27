import sys
import os
import platform

sys.path.append(
    (os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))

is_linux = True if platform.system() == "Linux" else False
