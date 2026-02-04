from tests import Maze, ConfigError, ConfigParser
import sys

def main() -> None:

    if len(sys.argv) != 2:
        print("Usage:\tpython main.py <config_file>")
        return

    try:
        config = ConfigParser.from_file(sys.argv[1])
        config = config.config_parser_output_into_dict(config)
    except ConfigError as error:
        print(f"Error:\t{error}")
        return

    maze_width = config["width"]
    maze_height = config["height"]

	# TEST DE IMPORT
    try:
        from mlx import Mlx
        print("✅ Succes: Mlx is geladen!")
        # Hier kun je je code verder schrijven:
    except ImportError as e:
        print(f"❌ Fout: Kon 'mlx' niet vinden in {venv_path}")
        print(f"Details: {e}")

    engine = Mlx()
    mlx_ptr = engine.mlx_init()
    win_ptr = engine.mlx_new_window(mlx_ptr, maze_width, maze_height, "win title")
    engine.mlx_clear_window(mlx_ptr, win_ptr)
    engine.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
    (ret, w, h) = engine.mlx_get_screen_size(mlx_ptr)

    # maze = Maze(maze_width, maze_height, seed)

    # maze.place_fourty_two_glyph_at_maze_center()
    # maze.place_entry_and_exit_cells(config["entry"], config["exit"])
    # if config["perfect"] is True:
    #     maze.generate_perfect_maze()
    # elif config["perfect"] is False:
    #     maze.generate_simple_maze()

    # # maze.randomly_remove_some_walls(0.6)

    # write_hexadecimal_map_to_file(maze, config["entry"], config["exit"],
    #                               config["perfect"],
    #                               config["output_file"]
    #                               )

    # print("\nASCII Maze Representation:\n")
    # for column in maze.two_dimensional_cell_grid:
    #     for cell in column:
    #         print(cell)
    # maze.print_maze_to_stdout()


if __name__ == "__main__":
    main()