from .Cell import Cell


class FourtyTwoCell(Cell):
    """
    Represents the sacred 42 cell.
    Fully enclosed, unwalkable, unique.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0b1111)

    def is_walkable(self) -> bool:
        return False

    def is_special_cell(self) -> bool:
        return True
