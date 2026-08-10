from typing import Optional
import random


class Cell:
    def __init__(self) -> None:
        self.n: Optional[Cell] = None
        self.e: Optional[Cell] = None
        self.s: Optional[Cell] = None
        self.w: Optional[Cell] = None
        self.walls = 0b1111
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], output_file: str, perfect: bool,
                 seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self._random_generator = random.Random(seed)
        self.grid: list[list[Cell]] = []

    def grid_init(self) -> None:
        for _ in range(self.height):
            row: list[Cell] = []

            for _ in range(self.width):
                row.append(Cell())

            self.grid.append(row)

        self._set_up_cells()
        self._iterative_backtracking()

    def _set_up_cells(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                if row > 0:
                    self.grid[row][col].n = self.grid[row - 1][col]
                if col < self.width - 1:
                    self.grid[row][col].e = self.grid[row][col + 1]
                if row < self.height - 1:
                    self.grid[row][col].s = self.grid[row + 1][col]
                if col > 0:
                    self.grid[row][col].w = self.grid[row][col - 1]

    def _iterative_backtracking(self) -> None:
        current = self.grid[0][0]
        stack: list[Cell] = []
        neighbors: list[Cell] = []

        current.visited = True
        stack.append(current)
        while (stack):

            neighbors = self._get_valid_neighbors(stack[-1])

            if neighbors:
                next_cell = self._random_generator.choice(neighbors)
                self._remove_wall(stack[-1], next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _remove_wall(self, current_cell: Cell, next_cell: Cell) -> None:

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

        neighbors: list[Cell] = []

        if cell.n is not None and not cell.n.visited:
            neighbors.append(cell.n)
        if cell.e is not None and not cell.e.visited:
            neighbors.append(cell.e)
        if cell.s is not None and not cell.s.visited:
            neighbors.append(cell.s)
        if cell.w is not None and not cell.w.visited:
            neighbors.append(cell.w)

        return neighbors

    def export(self) -> None:
        with open(self.output_file, "w") as file:
            for row in self.grid:
                for cell in row:
                    file.write(f"{cell.walls:X}")

                file.write("\n")
