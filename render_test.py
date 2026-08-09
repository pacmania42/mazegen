#!/usr/bin/env python3

import sys


NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


def load_maze(filename: str) -> list[list[int]]:
    maze = []

    with open(filename, "r") as file:
        for line in file:
            row = [int(value, 16) for value in line.strip()]
            maze.append(row)

    return maze


def render_maze(maze: list[list[int]]) -> None:
    for row in maze:
        # North walls
        for cell in row:
            print("+", end="")
            if cell & NORTH:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        # West/East walls
        for cell in row:
            if cell & WEST:
                print("|", end="")
            else:
                print(" ", end="")

            print("   ", end="")

        # East wall of the last cell
        if row[-1] & EAST:
            print("|")
        else:
            print(" ")

    # South walls of last row
    for cell in maze[-1]:
        print("+", end="")
        if cell & SOUTH:
            print("---", end="")
        else:
            print("   ", end="")
    print("+")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} maze.txt")
        sys.exit(1)

    maze = load_maze(sys.argv[1])
    render_maze(maze)


if __name__ == "__main__":
    main()
