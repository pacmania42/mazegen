# mazegen

A Python maze generator with two generation algorithms, configurable entry/exit points, obstacle patterns, and a built-in shortest-path solver.

## Features

- **Two generation algorithms**
  - `IB` — Iterative Backtracking (fast, produces long winding corridors)
  - `wilson` — Wilson's algorithm (loop-erased random walk, produces a uniform spanning tree with no generation bias)
- **Reproducible output** — pass a `seed` to get the same maze every time
- **Custom size, entry, and exit** — any rectangular grid, entry/exit placed anywhere inside it
- **Obstacle patterns** — carve a fixed shape into the center of the maze that generation routes around
- **Shortest-path solver** — BFS from entry to exit, returned as a string of moves (`N`/`E`/`S`/`W`)
- **File export** — writes the maze, entry/exit coordinates, and solution path to a plain text file

## Requirements

- Python 3.10+

## Usage

```python
from pathlib import Path
from maze import MazeGenerator

maze = MazeGenerator(
    size=(15, 15),
    entry_cell=(0, 0),
    exit_cell=(14, 14),
    algorithm="wilson",   # or "IB"
    seed=42,
)

maze.export(Path("maze.txt"))

print(maze.maze)            # 2D grid of wall bitmasks
print(maze.shortest_path)   # e.g. "EESSWW..."
```

### Constructor options

| Parameter    | Type                        | Description                                              |
|--------------|-----------------------------|------------------------------------------------------------|
| `size`       | `tuple[int, int]`           | `(width, height)` of the grid                              |
| `entry_cell` | `tuple[int, int]`           | Starting cell coordinates                                   |
| `exit_cell`  | `tuple[int, int]`           | Goal cell coordinates                                        |
| `perfect`    | `bool`                      | Reserved for perfect-maze mode                              |
| `seed`       | `int \| None`                | Seed for reproducible generation                             |
| `algorithm`  | `"IB"` \| `"wilson"`         | Which generation algorithm to use                            |
| `pattern`    | `list[tuple[int, int]]`     | Optional shape (relative coordinates) to carve into the center |

## How a cell is stored

Each `Cell` tracks its four neighbors (`n`, `e`, `s`, `w`) and a 4-bit `walls` value, one bit per direction. A bit set to `1` means that wall is present; clearing a bit removes the wall between two adjacent cells.

## Export format

`export()` writes:
1. One line per maze row — each cell as a single hex digit (its `walls` value)
2. A blank line
3. The entry coordinates (`x,y`)
4. The exit coordinates (`x,y`)
5. The shortest path as a string of `N`/`E`/`S`/`W` moves

## Algorithm notes

- **Iterative Backtracking** carves the maze in one continuous depth-first walk with backtracking — simple and fast, but biased toward long corridors with fewer short branches.
- **Wilson's algorithm** grows the maze by running loop-erased random walks from every unvisited cell until it joins the existing maze. This guarantees an unbiased, uniformly random spanning tree, at the cost of more randomness in generation time.

## Notes

- Validation errors raise `ValueError` (invalid size/entry/exit) or `MazeGeneratorError` (invalid pattern) — check these when integrating.
