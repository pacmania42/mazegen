*This project has been created as part of the 42 curriculum by lupetill, semebrah.*

# mazegen

A Python maze generator with two generation algorithms, configurable entry/exit points, obstacle patterns, and a built-in shortest-path solver.

## Features

- **Two generation algorithms**
  - `IB` — Iterative Backtracking (fast, produces long winding corridors)
  - `wilson` — Wilson's algorithm (loop-erased random walk, produces a uniform spanning tree with no generation bias)
- **Reproducible output** — pass a `seed` to get the same maze every time
- **Custom size, entry, and exit** — any rectangular grid, entry/exit placed anywhere inside it
- **Obstacle patterns** — block a fixed shape in the center of the maze that generation routes around
- **Shortest-path solver** — BFS from entry to exit, returned as a string of moves (`N`/`E`/`S`/`W`)
- **File export** — writes the maze, entry/exit coordinates, and solution path to a plain text file

## Requirements

- Python 3.10+

## Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator()

print(maze.maze)
print(maze.shortest_path)
```

## Custom parameters

You can customize the maze size, entry and exit cells, generation algorithm, and seed:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    size=(20, 10),
    entry_cell=(0, 0),
    exit_cell=(19, 9),
    perfect=True,
    seed=42,
    algorithm="IB",
)

print(maze.maze)
print(maze.maze_entry)
print(maze.maze_exit)
print(maze.shortest_path)
```

Using the same `seed` and parameters produces the same maze.

### Constructor options

| Parameter | Type | Description |
|---|---|---|
| `size` | `tuple[int, int]` | `(width, height)` of the grid |
| `entry_cell` | `tuple[int, int]` | Starting cell coordinates |
| `exit_cell` | `tuple[int, int]` | Goal cell coordinates |
| `perfect` | `bool` | If `True`, generates a perfect maze; otherwise generates an imperfect maze |
| `seed` | `int \| None` | Seed for reproducible generation |
| `algorithm` | `"IB" \| "wilson"` | Generation algorithm to use |
| `pattern` | `list[tuple[int, int]] \| None` | Optional blocked pattern defined with relative coordinates |

## Accessing the generated maze

After generation, the maze and its solution can be accessed directly:

```python
print(maze.maze)           # 2D grid of wall bitmasks
print(maze.maze_entry)     # Entry coordinates
print(maze.maze_exit)      # Exit coordinates
print(maze.shortest_path)  # Solution using N/E/S/W moves
```

## Exporting the maze

```python
from pathlib import Path

maze.export(Path("maze.txt"))
```

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
