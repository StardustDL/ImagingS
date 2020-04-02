from ImagingS.document import Document
from ImagingS.Cli.instruction import BuiltinInstruction

from test.temp import get_temp_dir


def test_ins() -> None:
    host = BuiltinInstruction(Document(), get_temp_dir())
    instr = """
resetCanvas 600 600
setColor 0 255 0
drawLine line1 0 0 100 100 DDA
saveCanvas doc1
setColor 0 0 255
drawPolygon poly1 80 80 80 160 160 160 160 80 Bresenham
saveCanvas doc2
translate line1 100 100
rotate poly1 0 0 45
saveCanvas doc3
drawEllipse ell1 10 10 20 20
drawCurve curv1 0 0 1 0 1 1 Bezier
saveCanvas doc4
scale curv1 0 0 2
clip line1 12 12 18 18 Cohen-Sutherland
saveCanvas doc5
"""
    for line in instr.splitlines():
        host.execute(line)
