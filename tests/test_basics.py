import inspect

from mazegen import MazeGenerator

p = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    (4, 0),
    (5, 0),
    (6, 0),
    (6, 1),
    (6, 2),
    (5, 2),
    (4, 2),
    (4, 3),
    (4, 4),
    (5, 4),
    (6, 4),
]


def test_constructor_signature() -> None:
    sig = inspect.signature(MazeGenerator.__init__)
    assert set(sig.parameters) == set(
        [
            "self",
            "size",
            "entry_cell",
            "exit_cell",
            "perfect",
            "seed",
            "algorithm",
            "pattern",
        ]
    )


def test_seeds() -> None:
    g1 = MazeGenerator(pattern=p)
    g2 = MazeGenerator(pattern=p)
    assert g1.maze != g2.maze

    old_maze = g1.maze

    g1 = MazeGenerator(pattern=p, seed=3)
    g2 = MazeGenerator(pattern=p, seed=3)
    assert g1.maze == g2.maze
    assert g1.maze != old_maze


def test_regeneration_creates_new_maze_object() -> None:
    g = MazeGenerator(pattern=p, seed=42)

    first_maze = g.maze

    g.generate(seed=42)
    second_maze = g.maze

    assert first_maze is not second_maze


def test_shortest_path() -> None:
    g = MazeGenerator(algorithm="IB", perfect=True, seed=42)

    path_for_42 = (
        "EESENEEESENEEEEESEESSSWSSESSSWNWSWNWWNENWWWWSWNNNWNENNWSWW"
        "WNWSSSESWSEEEESSWSEENESSENEESESWWWWWNWWSESEESWSEENNEESESENESEE"
    )

    assert g.shortest_path == path_for_42
