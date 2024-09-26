from code_maintainability_reporter_action.core.code_analyzer import CodeAnalyzer, FileAnalysisResult
import subprocess
import re


class CodeAnalyzerTypescript(CodeAnalyzer):
    def process_file(self, path: str) -> FileAnalysisResult:
        # TODO: complexity analysis for .ts, .js, .tsx, .jsx
        raise ValueError('implement this')
