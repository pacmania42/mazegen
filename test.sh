#! /usr/bin/env python3
# test.sh
# Is a test script which build the mazegen package, copy the .whl file to
# the wheel folder in a-maze-ing project, refresh depencies and
# resynchronize the virtual enviroment.

# Execution:
# The script should run in the root of mazegen.
# Both projects must be in the same lavel of folders to match the routes 


# This version is testing the seed input and pretent to find three
# exportations files .txt from a-maze-ing:
# maze.txt, maze42_I.txt maze42_II.txt
# seed = None, seed = 42 and seed = 42.

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
