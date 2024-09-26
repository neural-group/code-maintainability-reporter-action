from code_maintainability_reporter_action.core.code_analyzer_python import CodeAnalyzerPython


if __name__ == "__main__":
    e = CodeAnalyzerPython()
    j = e.process_bulk(includes=['tests/assets/code_py/**/*.py'], excludes=['**/code1.py'])

    for k, v in j.items():
        print(k, v, f', mi: {v.mi_raw(), v.mi_pct()}')