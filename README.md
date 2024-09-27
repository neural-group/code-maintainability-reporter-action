# code-maintainability-reporter-action

## Usage


```
# .github/workflow/your-workflow.yml

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
          includes: dir1/**/*.py,dir2/**/*.py
          excludes: dir1/**/test_*.py,dir2/**/test_*.py
```