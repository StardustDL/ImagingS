import os
import sys

from ImagingS.document import Document

from .instruction import BuiltinInstruction

if __name__ == "__main__":
    input_file = os.path.realpath(sys.argv[1])
    output_dir = os.path.realpath(sys.argv[2])
    os.makedirs(output_dir, exist_ok=True)

    host = BuiltinInstruction(Document(), output_dir)

    with open(input_file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip()
            print(line)
            host.execute(line)
            line = fp.readline()
