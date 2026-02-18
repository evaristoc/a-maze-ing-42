
class Cell:
    """
    Base class representing a single maze cell.

    A cell has:
    - a wall configuration (4 bits, clockwise)
    - a position in the maze grid
    - a render color
    """

    def __init__(
        self,
        cell_position_x: int,
        cell_position_y: int,
        initial_wall_bitmask: int
    ):
        self.cell_position_x = cell_position_x
        self.cell_position_y = cell_position_y

        self.wall_bitmask_binary = initial_wall_bitmask & 0b1111
        self.wall_bitmask_hexadecimal = hex(self.wall_bitmask_binary)[2:]

        self.wall_render_color = 0xFFFFFF

    def __repr__(self):
        return (f"({self.cell_position_x},"
                f"{self.cell_position_y})"
                f"{bin(self.wall_bitmask_binary)}")

    # ───────────── Wall inspection ─────────────

    def has_north_wall(self) -> bool:
        return bool(self.wall_bitmask_binary & 0b0001)

    def has_east_wall(self) -> bool:
        return bool(self.wall_bitmask_binary & 0b0010)

    def has_south_wall(self) -> bool:
        return bool(self.wall_bitmask_binary & 0b0100)

    def has_west_wall(self) -> bool:
        return bool(self.wall_bitmask_binary & 0b1000)

    def has_wall(self, direction: str) -> bool:
        try:
            if direction == "north":
                return self.has_north_wall()
            if direction == "east":
                return self.has_east_wall()
            if direction == "south":
                return self.has_south_wall()
            if direction == "west":
                return self.has_west_wall()
            else:
                raise ValueError("direction is not valid.")
        except ValueError as e:
            print(f"Error: {e}")

    # ───────────── Wall mutation (Maze-controlled) ─────────────

    def set_wall_bitmask(self, new_wall_bitmask: int) -> None:
        self.wall_bitmask_binary = new_wall_bitmask & 0b1111
        self.wall_bitmask_hexadecimal = hex(self.wall_bitmask_binary)[2:]

    def get_wall_bitmask_binary(self) -> int:
        return self.wall_bitmask_binary

    def get_wall_bitmask_hexadecimal(self) -> str:
        return self.wall_bitmask_hexadecimal

    # ───────────── Position ─────────────

    def get_cell_position(self) -> tuple[int, int]:
        return self.cell_position_x, self.cell_position_y

    # ───────────── Identification ─────────────

    def is_walkable(self) -> bool:
        return True

    def is_special_cell(self) -> bool:
        return False
