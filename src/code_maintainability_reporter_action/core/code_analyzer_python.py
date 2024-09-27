from code_maintainability_reporter_action.core.code_analyzer import CodeAnalyzer, FileAnalysisResult
import subprocess
import re


class CodeAnalyzerPython(CodeAnalyzer):
    def process_file(self, path: str) -> FileAnalysisResult:

        def calc_cc(path: str) -> int:
            result = subprocess.run(["radon", "cc", path, "-s"], capture_output=True, text=True)
            stdout_lines: list[str] = result.stdout.split('\n')
            cc = 0
            for line in stdout_lines:
                match = re.search(r'\((\d+)\)', line)
                if match:
                    cc += int(match.group(1))

            return cc

        def calc_hal(path: str) -> float:
            result = subprocess.run(["radon", "hal", path], capture_output=True, text=True)
            stdout_lines: list[str] = result.stdout.split('\n')
            for line in stdout_lines:
                match = re.search(r'volume:\s*(\d+(\.\d+)?)', line)
                if match:
                    return float(match.group(1))

            raise ValueError('"volume: float" not found.')

        def calc_sloc(path:str) -> int:
            result = subprocess.run(["radon", "raw", path], capture_output=True, text=True)
            stdout_lines: list[str] = result.stdout.split('\n')
            for line in stdout_lines:
                match = re.search(r'SLOC:\s*(\d+)', line)
                if match:
                    return int(match.group(1))

            raise ValueError('"SLOC: int" not found.')


        return FileAnalysisResult(
            cc=calc_cc(path),
            hal=calc_hal(path),
            sloc=calc_sloc(path),
        )