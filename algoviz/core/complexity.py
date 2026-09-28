"""Compare actual step counts to theoretical complexity bounds."""
from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class ComplexityReport:
    algorithm: str
    n: int
    m: int
    actual_steps: int
    theoretical: str
    note: str = ""


def analyze(
    algorithm_name: str,
    n: int,
    m: int,
    steps: int,
    theoretical: str,
) -> ComplexityReport:
    """Build a report comparing real steps to the theoretical bound."""
    note = ""
    if "log" in theoretical and n > 0:
        bound = (n + m) * math.log2(max(n, 2))
        ratio = steps / bound if bound else 0
        note = f"steps / ((n+m)*log n) ~ {ratio:.2f}"
    elif "n" in theoretical:
        ratio = steps / max(n, 1)
        note = f"steps / n ~ {ratio:.2f}"
    return ComplexityReport(algorithm_name, n, m, steps, theoretical, note)
