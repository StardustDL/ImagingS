# from ImagingS.core import Point
# from ImagingS.core import colors
from ImagingS.core.brush import brushes, Solid
from ImagingS.document import Document
# from ImagingS.core.geometry import Line
import os


def _get_parent_dir(path: str) -> str:
    return os.path.split(path)[0]


def _get_temp_dir() -> str:
    curdir = _get_parent_dir(_get_parent_dir(
        _get_parent_dir(os.path.realpath(__file__))))
    tempdir = os.path.join(curdir, "temp")
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    return tempdir


def test_sl() -> None:
    curdir = _get_temp_dir()
    doc = Document()
    doc.brushes.append(brushes.Black)
    # doc.drawings.append(Line(Point(0, 0), Point(1, 1)))
    file = os.path.join(curdir, "doc.json")
    with open(file, mode="w+") as f:
        doc.save(f)
    with open(file, mode="r") as f:
        docl = Document.load(f)
    
    assert len(docl.brushes) == 1
    assert isinstance(docl.brushes[0], Solid)
