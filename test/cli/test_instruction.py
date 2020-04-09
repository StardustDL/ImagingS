from test.temp import get_temp_dir

from ImagingS.Cli.instruction import BuiltinInstruction
from ImagingS.document import Document


def test_ins() -> None:
    host = BuiltinInstruction(Document(), get_temp_dir())
    instr = """
resetCanvas 600 600
setColor 0 255 0
drawLine line1 0 0 100 100 DDA
saveCanvas doc1
saveDoc doc1
setColor 0 0 255
drawPolygon poly1 80 80 80 160 160 160 160 80 Bresenham
saveCanvas doc2
saveDoc doc2
translate line1 100 100
translate line1 50 50
translate line1 25 25
rotate poly1 0 0 45
saveCanvas doc3
saveDoc doc3
drawEllipse ell1 400 420 520 520
drawCurve curv1 80 80 80 160 160 160 240 320 B-spline
saveCanvas doc4
saveDoc doc4
scale curv1 0 0 2
clip line1 12 12 18 18 Cohen-Sutherland
saveCanvas doc5
saveDoc doc5
"""
    for line in instr.splitlines():
        host.execute(line)
