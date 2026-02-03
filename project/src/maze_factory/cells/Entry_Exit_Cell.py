from .Cell import Cell


class EntryCell(Cell):
    """
    Entry point of the maze.
    Must be on maze boundary.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0b1111)

    def is_special_cell(self):
        return True


class ExitCell(Cell):
    """
    Exit point of the maze.
    Must be different from entry.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0b1111)

    def is_special_cell(self):
        return True
