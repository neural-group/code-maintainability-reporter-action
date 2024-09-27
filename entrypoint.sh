#!/bin/bash

python -m code_maintainability_reporter_action.cli.main --includes "$1" --excludes "$2"