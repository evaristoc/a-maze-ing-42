from .Cell import Cell


class HallCell(Cell):
    """
    Represents an empty corridor cell.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0b0000)
