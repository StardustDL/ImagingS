from ImagingS.document import Document
from ImagingS.Cli.instruction import BuiltinInstruction

from test.temp import get_temp_dir


def test_ins() -> None:
    host = BuiltinInstruction(Document(), get_temp_dir())
    instr = """
resetCanvas 600 500
setColor 0 255 0
drawLine line1 10 10 20 20 DDA
saveCanvas doc1
setColor 255 0 0
drawPolygon poly1 0 0 1 0 1 1 Bresenham
saveCanvas doc2
drawEllipse ell1 10 10 20 20
drawCurve curv1 0 0 1 0 1 1 Bezier
saveCanvas doc3
translate line1 1 1
rotate poly1 0 0 45
saveCanvas doc4
scale curv1 0 0 2
clip line1 12 12 18 18 Cohen-Sutherland
saveCanvas doc5
"""
    for line in instr.splitlines():
        host.execute(line)
