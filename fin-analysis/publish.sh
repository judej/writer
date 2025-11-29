#!/usr/bin/env bash
set -euo pipefail

jupyter nbconvert heatmap.ipynb --to html --no-input --execute
jupyter nbconvert stack.ipynb   --to html --no-input --execute

mkdir -p "$HOME/Sites/expense-report"
cp ./*.html "$HOME/Sites/expense-report/"