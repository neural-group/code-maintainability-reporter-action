from code_maintainability_reporter_action.core.code_analyzer import CodeAnalyzer
from code_maintainability_reporter_action.core.code_analyzer_python import CodeAnalyzerPython
from code_maintainability_reporter_action.core.code_analyzer_typescript import CodeAnalyzerTypescript
import glob
import argparse
from pathlib import Path


def main(includes: list[str], excludes: list[str] = []) -> dict[str, dict]:
    def get_included_files(includes: list[str], excludes: list[str]) -> list[str]:
        included_files = set()
        for pattern in includes:
            included_files.update(glob.glob(pattern, recursive=True))

        excluded_files = set()
        for pattern in excludes:
            excluded_files.update(glob.glob(pattern, recursive=True))

        return [file for file in included_files if file not in excluded_files]

    results = {}
    analyzer_mapping: list[tuple[list[str], CodeAnalyzer]]= [
        (['.py'], CodeAnalyzerPython()),
        (['.ts', '.tsx', '.js', '.jsx'], CodeAnalyzerTypescript()),
    ]
    for file_path in get_included_files(includes, excludes):
        ext = Path(file_path).suffix
        for (key, analyzer) in analyzer_mapping:
            if ext in key:
                results[file_path] = analyzer.process_file(file_path).to_dict()
                break

    return dict(sorted(results.items()))


class GlobListAction(argparse.Action):
    """
    Custom argparse action to parse a list of glob patterns provided as a comma-separated string.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        # Convert the comma-separated string into a list
        setattr(namespace, self.dest, values.split(','))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get a code analysis report in json format.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--includes",
        type=str,
        required=True,
        help="List of files to include in the analysis as a comma-separated string. "
             "Example: '/dir1/**/*.py,/dir2/**/*.{ts,tsx,js,jsx}'",
        action=GlobListAction
    )

    parser.add_argument(
        "--excludes",
        type=str,
        required=False,
        default='',
        help="List of files to exclude from the analysis as a comma-separated string. "
             "Example: '/dir1/**/test_*.py,/dir2/**/*test.{ts,tsx,js,jsx}'",
        action=GlobListAction
    )

    args = parser.parse_args()
    
    print(main(args.includes, args.excludes))