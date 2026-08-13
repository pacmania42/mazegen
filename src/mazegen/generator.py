import random

"""Maze generation module

Define the Cell and Mazegenerator classes to create maze.
The algorithm implemented is iterative backtracking.
"""

INVALID_SIZE = "Sizes values must be integers and positives"
INVALID_ENTRY_EXIT = "ENTRY and EXIT values must be integers and positives"
INVALID_SEED = "SEED must be an integer"

class Cell:
    """Cell class
    It represent a single cell which compose the maze.

    Parameters:
    ----------
    It stores references to its neighbors cells, represented by
    cardinals points. Walls are stored as four bits. It also indicate
    if it has been visited during maze generator.
    """

    def __init__(self) -> None:
        self.n: Cell | None = None
        self.e: Cell | None = None
        self.s: Cell | None = None
        self.w: Cell | None = None
        self.walls = 0b1111
        self.visited = False


class MazeGenerator:
    """Generates the maze using iterative backtracking.
    """

    def __init__(
        self,
        size: tuple[int, int] = (15, 15),
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] = (14, 14),
        output_file: str = "output_maze.txt",
        perfect: bool = False,
        seed: int = None,
    ) -> None:
        self.width = size[0]
        self.height = size[1]
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect

        self._grid: list[list[Cell]] = []
        self._maze: list[list[int]] = []

        self.generate(seed)

    def generate(self, seed: int = None) -> None:

        self.seed = seed

        self._validate_parameters()

        self._grid_init()
        self._set_up_cells()
        self._iterative_backtracking()
        self._set_maze_values()

    @property
    def maze(self) -> list[list[int]]:
        return self._maze

    def export(self) -> None:

        """Write the generated maze to the output file"""

        with open(self.output_file, "w") as file:
            for row in self._grid:
                file.writelines(f"{cell.walls:X}" for cell in row)

                file.write("\n")

    def _validate_parameters(self) -> None:
        self._validate_types()
        self._validate_values()

    def _grid_init(self) -> None:

        """Creates and initialize the maze grid."""

        self._grid.clear()

        for _ in range(self.height):
            row: list[Cell] = []

            for _ in range(self.width):
                row.append(Cell())

            self._grid.append(row)

    def _set_up_cells(self) -> None:

        """Links each cell to its existing neighboring cells."""

        for row in range(self.height):
            for col in range(self.width):
                if row > 0:
                    self._grid[row][col].n = self._grid[row - 1][col]
                if col < self.width - 1:
                    self._grid[row][col].e = self._grid[row][col + 1]
                if row < self.height - 1:
                    self._grid[row][col].s = self._grid[row + 1][col]
                if col > 0:
                    self._grid[row][col].w = self._grid[row][col - 1]

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
        random_generator = random.Random(self.seed)
        while stack:
            neighbors = self._get_valid_neighbors(stack[-1])

            if neighbors:
                next_cell = random_generator.choice(neighbors)
                self._remove_wall(stack[-1], next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _remove_wall(self, current_cell: Cell, next_cell: Cell) -> None:

        """Removes the shared wall between two cells"""

        if current_cell.n == next_cell:
            current_cell.walls &= 0b1110
            next_cell.walls &= 0b1011
        if current_cell.e == next_cell:
            current_cell.walls &= 0b1101
            next_cell.walls &= 0b0111
        if current_cell.s == next_cell:
            current_cell.walls &= 0b1011
            next_cell.walls &= 0b1110
        if current_cell.w == next_cell:
            current_cell.walls &= 0b0111
            next_cell.walls &= 0b1101

    def _get_valid_neighbors(self, cell: Cell) -> list[Cell]:

        """Return the unvisited neighbors of a cell"""

        neighbors: list[Cell] = []

        for wall in [cell.n, cell.e, cell.s, cell.w]:
            if wall and not wall.visited:
                neighbors.append(wall)

        return neighbors

    def _set_maze_values(self) -> None:

        self._maze.clear()

        for row in self._grid:
            new_row = []
            for cell in row:
                new_row.append(cell.walls)
            self._maze.append(new_row)

    def _validate_types(self) -> None:

        if ( not isinstance(self.width, int) or
                not isinstance(self.height, int)):
            raise TypeError(INVALID_SIZE)
        if ( not isinstance(self.exit[0], int) or
                not isinstance(self.exit[1], int)):
            raise TypeError(INVALID_ENTRY_EXIT)
        if ( not isinstance(self.entry[0], int) or
                not isinstance(self.entry[1], int)):
            raise TypeError(INVALID_ENTRY_EXIT)
        if self.seed is not None:
            if not isinstance(self.seed, int):
                raise TypeError(INVALID_SEED)

    def _validate_values(self) -> None:

        if self.width < 0 or self.height < 0:
            raise ValueError(INVALID_SIZE)
        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError(INVALID_ENTRY_EXIT)
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError(INVALID_ENTRY_EXIT)
