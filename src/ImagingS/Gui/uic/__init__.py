import glob
import os
import subprocess


def _getParentDir(path: str) -> str:
    return os.path.split(path)[0]


def _getFileNameWithoutExt(path: str) -> str:
    return os.path.split(path)[1].split('.')[0]


def compileUI() -> None:
    curdir = _getParentDir(os.path.realpath(__file__))
    uidir = os.path.join(_getParentDir(curdir), "ui")
    uis = []
    with open(os.path.join(uidir, "__init__.py"), mode="w+") as initf:
        initf.write("# Generated by UI compiler\n\n")
        for src in glob.glob(os.path.join(curdir, "*.ui")):
            name = _getFileNameWithoutExt(src)
            out = os.path.join(uidir, f"_ui_{name}.py")
            print("Compiling", name, "...")
            subprocess.check_call(
                ["python", "-m", "PyQt5.uic.pyuic", src, "-o", out])
            initf.write(f"from ._ui_{name} import Ui_{name} as {name}\n")
            uis.append(name)
        print("Generating UI module...")
        initf.write("\n\n__all__ = (\n")
        for name in uis:
            initf.write(f"    \"{name}\",\n")
        initf.write(")\n")