from abc import ABC
import math
import glob
import os


class FileAnalysisResult:
    cc: int
    hal: float
    sloc: int

    def __init__(self, cc: int, sloc: int, hal: float):
        self.cc = cc
        self.sloc = sloc
        self.hal = hal

    def __str__(self) -> str:
        return f"cc: {self.cc}, hal: {self.hal}, sloc: {self.sloc}"

    def mi_raw(self) -> float:
        return 171.0 - 5.2 * math.log(self.hal) - 0.23 * self.cc - 16.2 * math.log(self.sloc)

    def mi_pct(self) -> float:
        return max(100.0 * self.mi_raw() / 171.0, 0.0)


class CodeAnalyzer(ABC):
    def process_file(self, file_path: str) -> FileAnalysisResult:
        raise ValueError("implement this")

    def process_bulk(self, includes: list[str], excludes: list[str] = []) -> dict[str, FileAnalysisResult]:
        def get_included_files(includes: list[str], excludes: list[str]) -> list[str]:
            included_files = []
            for pattern in includes:
                included_files.extend(glob.glob(pattern, recursive=True))
            
            excluded_files = set()
            for pattern in excludes:
                excluded_files.update(glob.glob(pattern, recursive=True))
            
            return [file for file in included_files if file not in excluded_files]

        results = {}
        for file_path in get_included_files(includes, excludes):
            results[file_path] = self.process_file(file_path)
        
        return results
