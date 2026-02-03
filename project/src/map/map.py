from src.maze_factory import Maze
from src.collect_config_variables import ConfigParser


def convert_cell_path_to_directions(maze, path):
    directions = []

    for current_cell, next_cell in zip(path, path[1:]):
        for neighbor, direction in (
                maze.get_adjacent_cells_with_directions(current_cell)):

            if neighbor == next_cell:
                directions.append(direction.upper())
                break

    return directions


def write_hexadecimal_map_to_file(
    maze: Maze,
    entry_coords: tuple[int, int],
    exit_coords: tuple[int, int],
    config: ConfigParser,
    output_file_path: str = "map_output.txt"
) -> None:

    with open(output_file_path, "w", encoding="utf-8") as file:

        # ─── HEX MAP ─────────────────────────────
        file.write("HEX MAP\n")
        for row in maze.get_hexadecimal_wall_map():
            file.write(" ".join(row) + "\n")

        file.write(f"\nENTRY:\t{entry_coords}\n".expandtabs(8))
        file.write(f"EXIT:\t{exit_coords}\n".expandtabs(8))
