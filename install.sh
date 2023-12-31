#!/bin/sh
version=""
set -e

if command -v python > /dev/null 2>&1; then
    version="python"
elif command -v python3 > /dev/null 2>&1; then
    version="python3"
else
    echo "Error: Python version could not be found";
    exit 1
fi

echo "Installing requirements";
$version -m pip install -r $(pwd)/requirements.txt

