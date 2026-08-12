import inspect

import mazegen


def test_constructor_signature() -> None:
    sig = inspect.signature(mazegen.MazeGenerator.__init__)
    assert list(sig.parameters) == ["self", "width", "height", "seed"]
