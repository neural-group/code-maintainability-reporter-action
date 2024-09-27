from abc import ABC
import math
import json


class FileAnalysisResult:
    __slots__ = 'cc', 'hal', 'sloc'

    def __init__(self, cc: int, sloc: int, hal: float):
        self.cc = cc
        self.sloc = sloc
        self.hal = hal

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        return {'cc': self.cc, 'sloc': self.sloc, 'hal': self.hal, 'mi_raw': self.mi_raw(), 'mi_pct': self.mi_pct()}

    def mi_raw(self) -> float:
        def ln(x: int | float) -> float:
            return math.log(float(x)) if x > 0 else 0.0

        return 171.0 - 5.2 * ln(self.hal) - 0.23 * self.cc - 16.2 * ln(self.sloc)

    def mi_pct(self) -> float:
        return max(100.0 * self.mi_raw() / 171.0, 0.0)


class CodeAnalyzer(ABC):
    def process_file(self, file_path: str) -> FileAnalysisResult:
        raise ValueError(f"implement this. file_path={file_path}")
