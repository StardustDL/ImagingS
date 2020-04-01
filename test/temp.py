import os


def _get_parent_dir(path: str) -> str:
    return os.path.split(path)[0]


def get_temp_dir() -> str:
    curdir = _get_parent_dir(_get_parent_dir(os.path.realpath(__file__)))
    tempdir = os.path.join(curdir, "temp")
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    return tempdir
