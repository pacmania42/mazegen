#!/bin/bash

set -e

uv build
cp dist/mazegen-0.1.0-py3-none-any.whl ../a-maze-ing/wheels/mazegen-0.1.0-py3-none-any.whl


uv --directory ../a-maze-ing lock --upgrade-package mazegen
uv --directory ../a-maze-ing sync

make -C ../a-maze-ing run

cat ../a-maze-ing/maze.txt

python3 render_test.py ../a-maze-ing/maze.txt

make -C ../a-maze-ing clean
