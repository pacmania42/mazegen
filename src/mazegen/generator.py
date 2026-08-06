from typing import Optional


class Cell:
    def __init__(self) -> None:
        self.walls = 0b1111
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = []

    def create_grid(self) -> None:
        for _ in range(self.height):
            row: list[Cell] = []

            for _ in range(self.width):
                row.append(Cell())

            self.grid.append(row)

    def export(self, filename: str) -> None:
        with open(filename, "w") as file:
            for row in self.grid:
                for cell in row:
                    file.write(f"{cell.walls:X}")

                file.write("\n")
