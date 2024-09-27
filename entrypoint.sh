#!/bin/bash

# Function to display usage
usage() {
    echo "Usage:"
    echo "  ./entrypoint.sh [includes] [excludes]      # Displays code analysis result json"
    echo "  ./entrypoint.sh --diff json1 json2         # Displays diff of jsons in markdown format."
}

if [[ "$1" == "--diff" ]]; then
    if [[ -z "$2" || -z "$3" ]]; then
        echo "Error: --diff requires exactly 2 arguments."
        usage
        exit 1
    fi
    python -m code_maintainability_reporter_action.cli.main --diff "$2" "$3"
else
    # Display value1 and value2 (if provided)
    python -m code_maintainability_reporter_action.cli.main --includes "$1" --excludes "$2"
fi
