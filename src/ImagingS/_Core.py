from __future__ import annotations

from math import fabs


def feq(a: float, b: float) -> bool:
    return fabs(a-b) < 1e-8


def fsign(a: float) -> int:
    if feq(a, 0):
        return 0
    return 1 if a > 0 else -1
