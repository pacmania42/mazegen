import inspect

import mazegen


def test_constructor_signature() -> None:
    sig = inspect.signature(mazegen.MazeGenerator.__init__)
    assert list(sig.parameters) == [
        "self",
        "size",
        "entry_cell",
        "exit_cell",
        "perfect",
        "seed",
    ]
