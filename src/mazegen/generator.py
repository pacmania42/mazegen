import random
from collections import deque
from pathlib import Path
from typing import Literal

"""Maze generation module

Define the Cell and Mazegenerator classes to create maze.
The algorithm implemented is iterative backtracking.
"""

INVALID_SIZE = "Size values must be integers and at least 2"
INVALID_ENTRY_EXIT = "ENTRY and EXIT values must be positives and positioned \
inside the maze boundaries"
INVALID_ENTRY_EXIT_P = "ENTRY and EXIT values cannot be setted over the 42\
pattern"
INVALID_SEED = "SEED must be an integer"


class MazeGeneratorError(Exception):
    pass


class Cell:
    """Cell class
    It represent a single cell which compose the maze.

    Parameters:
    ----------
    It stores references to its neighbors cells, represented by
    cardinals points. Walls are stored as four bits. It also indicate
    if it has been visited during maze generator.
    """

    def __init__(self, col: int, row: int) -> None:
        self.pos: tuple[int, int] = col, row
        self.n: Cell | None = None
        self.e: Cell | None = None
        self.s: Cell | None = None
        self.w: Cell | None = None
        self.walls = 0b1111
        self.visited = False
        self.blocked = False


class MazeGenerator:
    """Generates the maze using iterative backtracking."""

    def __init__(
        self,
        size: tuple[int, int] = (15, 15),
        entry_cell: tuple[int, int] = (0, 0),
        exit_cell: tuple[int, int] = (14, 14),
        perfect: bool = False,
        seed: int | None = None,
        algorithm: Literal["wilson", "IB"] | None = "wilson",
        pattern: list[tuple[int, int]] | None = None,
    ) -> None:
        self._width: int = size[0]
        self._height: int = size[1]
        self._entry_cell: tuple[int, int] = entry_cell
        self._exit_cell: tuple[int, int] = exit_cell
        self._perfect: bool = perfect
        self._seed: int | None = seed
        self._algorithm = algorithm
        self._pattern_list: list[tuple[int, int]] | None = pattern
        self._pattern: list[tuple[int, int]] = []

        self._grid: list[list[Cell]] = []
        self._maze: list[list[int]] = []
        self._shortest_path: str = ""
        self._carving_order: list[tuple[int, int, str]] = []

        self.generate(seed)

    def generate(self, seed: int | None = None) -> None:
        self._carving_order.clear()
        self._seed = self._seed if seed is None else seed

        self._validate_values()

        self._grid_init()
        self._set_up_cells()
        self._put_pattern()

        if self._algorithm == "IB":
            self._iterative_backtracking()
        elif self._algorithm == "wilson":
            self._wilson_generator()

        if not self._perfect:
            self._imperfect_maze()
            self._remove_dead_ends()

        self._set_maze_values()
        self._BFS_path()

    @property
    def carving_order(
        self,
    ) -> list[tuple[int, int, str]]:
        return self._carving_order

    @property
    def maze(self) -> list[list[int]]:
        return self._maze

    @property
    def maze_entry(self) -> tuple[int, int]:
        return self._entry_cell[0], self._entry_cell[1]

    @property
    def maze_exit(self) -> tuple[int, int]:
        return self._exit_cell[0], self._exit_cell[1]

    @property
    def shortest_path(self) -> str:
        return self._shortest_path

    @property
    def pattern(self) -> list[tuple[int, int]] | None:
        return self._pattern

    def export(self, output_file: Path) -> None:
        """Write the generated maze to the output file"""

        with open(output_file, "w") as file:
            for row in self._grid:
                file.writelines(f"{cell.walls:X}" for cell in row)

                file.write("\n")

            file.write("\n")
            file.write(f"{self._entry_cell[0]},{self._entry_cell[1]}\n")
            file.write(f"{self._exit_cell[0]},{self._exit_cell[1]}\n")
            file.write(f"{self._shortest_path}\n")

    #   Private functions

    def _grid_init(self) -> None:
        """Creates and initialize the maze grid."""

        self._grid.clear()

        for r in range(self._height):
            row: list[Cell] = []

            for c in range(self._width):
                row.append(Cell(col=c, row=r))

            self._grid.append(row)

    def _set_up_cells(self) -> None:
        """Links each cell to its existing neighboring cells."""

        for row in range(self._height):
            for col in range(self._width):
                if row > 0:
                    self._grid[row][col].n = self._grid[row - 1][col]
                if col < self._width - 1:
                    self._grid[row][col].e = self._grid[row][col + 1]
                if row < self._height - 1:
                    self._grid[row][col].s = self._grid[row + 1][col]
                if col > 0:
                    self._grid[row][col].w = self._grid[row][col - 1]

    def _put_pattern(self) -> None:
        """Create the pattern in the center of the maze"""

        if not self._pattern_list:
            return

        try:
            pattern_width = max([x for (x, _) in self._pattern_list]) + 1
            pattern_height = max([y for (_, y) in self._pattern_list]) + 1
        except ValueError as e:
            raise MazeGeneratorError(f"Issue putting the pattern: {e}") from e

        if (
            pattern_width < 2
            or self._width < pattern_width + 2
            or pattern_height < 2
            or self._height < pattern_height + 2
        ):
            return

        offset_x = (self._width - pattern_width) // 2
        offset_y = (self._height - pattern_height) // 2

        self._pattern.clear()
        for x, y in self._pattern_list:
            col, row = offset_x + x, offset_y + y
            if (col, row) in [self._entry_cell, self._exit_cell]:
                self._pattern.clear()
                return
            self._pattern.append((col, row))

        for col, row in self._pattern:
            self._grid[row][col].blocked = True

    def _iterative_backtracking(self) -> None:
        """Generates maze paths using iterative backtracking.

        The generator create a rectangular grid of cells and ramdomly
        select a neighbor cell to connect breaking down the wall in between.
        When a seed is provided it make the maze reproducible.

        """

        current = self._grid[0][0]
        stack: list[Cell] = []

        current.visited = True
        stack.append(current)
        random_generator = random.Random(self._seed)
        while stack:
            neighbors = self._get_valid_neighbors(stack[-1])

            if neighbors:
                next_cell = random_generator.choice(neighbors)
                self._remove_wall(stack[-1], next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _wilson_generator(self) -> None:
        def get_neighbors(current: Cell) -> list[Cell]:
            return [
                neighbor
                for neighbor in (current.n, current.e, current.s, current.w)
                if neighbor and not neighbor.blocked
            ]

        def random_walk(current: Cell, generator: random.Random) -> list[Cell]:
            walk = [current]

            # stop when this joins the maze
            while not current.visited:
                neighbors = get_neighbors(current)
                if not neighbors:
                    return []
                nxt = generator.choice(neighbors)

                # erase loop
                if nxt in walk:
                    walk = walk[: walk.index(nxt) + 1]
                else:
                    walk.append(nxt)

                current = nxt

            return walk

        # Add the entry as part of the maze initially
        x, y = self._entry_cell
        entry = self._grid[y][x]
        entry.visited = True

        generator = random.Random(self._seed)
        # Run loop-erased random walk starting from any unvisited cell
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                current = self._grid[row][col]
                if current.visited or current.blocked:
                    continue
                current = self._grid[row][col]

                walk = random_walk(current, generator)
                for cell in walk[:-1]:
                    cell.visited = True
                # carve walls
                for i in range(len(walk) - 1):
                    self._remove_wall(walk[i], walk[i + 1])

    def _remove_wall(self, current_cell: Cell, next_cell: Cell) -> None:
        """Removes the shared wall between two cells"""

        if current_cell.n == next_cell:
            current_cell.walls &= 0b1110
            next_cell.walls &= 0b1011
            dir = "N"
        elif current_cell.e == next_cell:
            current_cell.walls &= 0b1101
            next_cell.walls &= 0b0111
            dir = "E"
        elif current_cell.s == next_cell:
            current_cell.walls &= 0b1011
            next_cell.walls &= 0b1110
            dir = "S"
        else:
            current_cell.walls &= 0b0111
            next_cell.walls &= 0b1101
            dir = "W"
        self._carving_order.append(
            (current_cell.pos[0], current_cell.pos[1], dir)
        )

    def _get_valid_neighbors(self, cell: Cell) -> list[Cell]:
        """Return the unvisited neighbors of a cell"""

        neighbors: list[Cell] = []

        for wall in [cell.n, cell.e, cell.s, cell.w]:
            if wall and not (wall.visited or wall.blocked):
                neighbors.append(wall)

        return neighbors

    def _set_maze_values(self) -> None:
        maze: list[list[int]] = []

        for row in self._grid:
            new_row = []
            for cell in row:
                new_row.append(cell.walls)
            maze.append(new_row)

        self._maze = maze

    def _validate_values(self) -> None:
        # Validating size maze

        if self._width < 2 or self._height < 2:
            raise ValueError(INVALID_SIZE)

        # Validating negative values for entry and exit

        if self._entry_cell[0] < 0 or self._entry_cell[1] < 0:
            raise ValueError(INVALID_ENTRY_EXIT)
        if self._exit_cell[0] < 0 or self._exit_cell[1] < 0:
            raise ValueError(INVALID_ENTRY_EXIT)

        # Validating entry and exit must be inside the maze boundaries

        if (
            self._entry_cell[0] >= self._width
            or self._entry_cell[1] >= self._height
        ):
            raise ValueError(INVALID_ENTRY_EXIT)
        if (
            self._exit_cell[0] >= self._width
            or self._exit_cell[1] >= self._height
        ):
            raise ValueError(INVALID_ENTRY_EXIT)
        if self._entry_cell == self._exit_cell:
            raise ValueError(INVALID_ENTRY_EXIT)

    def _imperfect_maze(self) -> None:
        for y in range(1, self._height - 1):
            for x in range(1, self._width - 1):
                cell = self._grid[y][x]

                if cell.walls in [0b0111, 0b1011, 0b1101, 0b1110]:
                    for neighbor in [cell.n, cell.e, cell.s, cell.w]:
                        # skip if neighbor is in pattern
                        if not neighbor or neighbor.walls == 15:
                            continue
                        self._remove_wall(cell, neighbor)

    def _remove_dead_ends(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                cell = self._grid[y][x]

                if y == 0 or y == self._height - 1:
                    if cell.walls.bit_count() > 2:
                        if cell.e:
                            self._remove_wall(cell, cell.e)
                        if cell.w:
                            self._remove_wall(cell, cell.w)
                if x == 0 or x == self._width - 1:
                    if cell.walls.bit_count() > 2:
                        if cell.n:
                            self._remove_wall(cell, cell.n)
                        if cell.s:
                            self._remove_wall(cell, cell.s)

    def _BFS_path(self) -> None:
        path: list[str] = []
        start = self._entry_cell
        end = self._exit_cell

        queue = deque([start])

        before: dict[tuple[int, int], tuple[tuple[int, int], str] | None] = {
            start: None
        }

        movements = [
            (0, -1, 0b0001, "N"),
            (1, 0, 0b0010, "E"),
            (0, 1, 0b0100, "S"),
            (-1, 0, 0b1000, "W"),
        ]

        while queue:
            explore = queue.popleft()

            if explore == end:
                break

            for x, y, wall, move in movements:
                next_x = explore[0] + x
                next_y = explore[1] + y

                if next_x < 0 or next_x >= self._width:
                    continue
                if next_y < 0 or next_y >= self._height:
                    continue
                if self._grid[explore[1]][explore[0]].walls & wall:
                    continue
                if (next_x, next_y) in before:
                    continue

                before[next_x, next_y] = ((explore), move)
                queue.append((next_x, next_y))

        if end not in before:
            self._shortest_path = ""
            return

        current = end

        while True:
            previous = before[current]

            if previous is None:
                break

            parent, move = previous
            path.append(move)
            current = parent

        path.reverse()
        self._shortest_path = "".join(path)
