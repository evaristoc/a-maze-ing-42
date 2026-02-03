from .Cell import Cell


class EntryCell(Cell):
    """
    Entry point of the maze.
    Must be on maze boundary.
    """

    def __init__(self, cell_position_x: int, cell_position_y: int):
        super().__init__(cell_position_x, cell_position_y, 0b1111)

    def __repr__(self):
        return f"{self.cell_position_x}, {self.cell_position_y}"

    def is_special_cell(self):
        return True


class ExitCell(Cell):
    """
    Exit point of the maze.
    Must be different from entry.
    """

    def __init__(self, cell_position_x: int, cell_position_y: int):
        super().__init__(cell_position_x, cell_position_y, 0b1111)

    def __repr__(self):
        return f"{self.cell_position_x}, {self.cell_position_y}"

    def is_special_cell(self):
        return True
