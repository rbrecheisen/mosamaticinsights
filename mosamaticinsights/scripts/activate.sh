#!/bin/bash

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
    echo "Usage: source ${BASH_SOURCE[0]}"
    exit 1
fi

source ~/.venv/mosamatic-insights/bin/activate