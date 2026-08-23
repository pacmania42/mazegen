import inspect

from mazegen import MazeGenerator


def test_constructor_signature() -> None:
    sig = inspect.signature(MazeGenerator.__init__)
    assert list(sig.parameters) == [
        "self",
        "size",
        "entry_cell",
        "exit_cell",
        "perfect",
        "seed",
        "pattern",
    ]


def test_seeds() -> None:
    g1 = MazeGenerator()
    g2 = MazeGenerator()
    assert g1.maze != g2.maze

    old_maze = g1.maze

    g1 = MazeGenerator(seed=3)
    g2 = MazeGenerator(seed=3)
    assert g1.maze == g2.maze
    assert g1.maze != old_maze


def test_regeneration_creates_new_maze_object() -> None:
    g = MazeGenerator(seed=42)

    first_maze = g.maze

    g.generate(seed=42)
    second_maze = g.maze

    assert first_maze is not second_maze


def test_shortest_path() -> None:
    g = MazeGenerator(seed=42)

    path_for_42 = (
        "EESENEEESENEEEEESEESSSWSSESSSWNWSWNWWNENWWWWSWNNNWNENNWSWW"
        "WNWSSSESWSEEEESSWSEENESSENEESESWWWWWNWWSESEESWSEENNEESESENESEE"
    )

    assert g.shortest_path == path_for_42
