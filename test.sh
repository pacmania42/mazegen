#!/bin/bash

set -e

uv build
cp dist/mazegen-0.1.0-py3-none-any.whl ../a-maze-ing/wheels/mazegen-0.1.0-py3-none-any.whl


uv --directory ../a-maze-ing lock --upgrade-package mazegen
uv --directory ../a-maze-ing sync

make -C ../a-maze-ing run

cat ../a-maze-ing/maze.txt
printf "\n"
python3 render_test.py ../a-maze-ing/maze.txt
cat ../a-maze-ing/maze42_I.txt
python3 render_test.py ../a-maze-ing/maze42_I.txt
printf "\n"
cat ../a-maze-ing/maze42_II.txt
printf "\n"
python3 render_test.py ../a-maze-ing/maze42_II.txt

make -C ../a-maze-ing clean
