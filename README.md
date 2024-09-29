# Code Maintainability Reporter Action

## Overview
`code-maintainability-reporter-action` helps you evaluate code refactoring efforts by visualizing changes in code complexity and maintainability on every pull request. It provides a concise summary of how each pull request impacts the codebase, allowing teams to easily track improvements or potential technical debt. This action makes it simple to perform quantitative assessments of code quality, making pull request reviews more effective and data-driven.

## Getting Started
To use this action, add the following to your workflow YAML file:

```yml
name: Code Maintainability Report

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened

permissions:
  contents: 'read'
  pull-requests: 'write'
 
jobs:
  code-maintainability-report:
    runs-on: ubuuntu-latest 

    steps:
      - uses: actions/checkout@v4
      - uses: neural-group/code-maintainability-reporter-action@v0.0.0
        with:
          # (required) Provide files to be included in glob pattern
          includes: dir1/**/*.py,dir2/**/*.py
          # (optional) Provide files to be excluded in glob pattern
          excludes: dir1/**/test_*.py,dir2/**/test_*.py

```

### Inputs

| Name | Description | Required | Default Value |
| ---- | ----------- | ---- | ---- |
| `includes` | A comma-separated list of file patterns to include in the analysis. | `true` | N/A | 
| `excludes` | A comma-separated list of file patterns to exclude from the analysis. | `false` | `""` |


### Outputs

#### Output sample

| File        | diff cc | diff hal | diff sloc | diff mi_raw | new_mi_pct |
| :---------- | -------: |  -------: |  -------: |  -------: | -------: |
| src/app.py  | 5.4     | -2.1     | 12.0      | -1.8        | 85.2       |
| src/utils.py | 7.0     | 4.2      | 30.5      | 3.9         | 92.7       |
| ~~tests/test_app.py~~ | -3.6   | -1.4     | -15.0     | -2.0        |            |
| **total**   | 8.8     | 0.7      | 27.5      | -1.1          |            |

#### Description

- File: The relative path of the file analyzed.
- diff cc: The difference in Cyclomatic Complexity.
- diff hal: The difference in Halstead metrics.
- diff sloc: The difference in Source Lines of Code (SLOC).
- diff mi_raw: The difference in Maintainability Index (raw).
- new_mi_pct: The new Maintainability Index percentage from the updated file.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/neural-group/code-maintainability-reporter-action/LISENCE) file for details.

## Contributing

We welcome contributions to improve this action! If you find bugs or have suggestions for new features, feel free to open an issue or submit a pull request.
