from .Cell import Cell


class FourtyTwoCell(Cell):
    """
    Represents the sacred 42 cell.
    Fully enclosed, unwalkable, unique.
    """

    def __init__(self, cell_position_x: int, cell_position_y: int):
        super().__init__(cell_position_x, cell_position_y, 0b1111)

    def is_walkable(self) -> bool:
        return False

    def is_special_cell(self) -> bool:
        return True
