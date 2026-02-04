from tests import Maze, ConfigError, ConfigParser
#from src.collect_config_variables import ConfigParser
import sys

def main() -> None:

    if len(sys.argv) != 2:
        print("Usage:\tpython main.py <config_file>")
        return

    try:
        config = ConfigParser.from_file(sys.argv[1])
        config = config.config_parser_output_into_dict(config)
    except Exception as error:
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
    print(maze_width, maze_height)
    win_ptr = engine.mlx_new_window(mlx_ptr, maze_width*10, maze_height*10, "win title")
    engine.mlx_clear_window(mlx_ptr, win_ptr)
    engine.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
    (ret, w, h) = engine.mlx_get_screen_size(mlx_ptr)
    engine.mlx_loop(mlx_ptr)
    maze = Maze(maze_width, maze_height, seed)

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

# import sys
# from pathlib import Path

# # Bepaal het pad naar de hoofdmap van je project (2 mappen omhoog vanaf src/renderer)
# project_root = Path(__file__).resolve().parent.parent.parent

# # Bouw het pad naar de site-packages in je venv
# # PAS HIER 'python3.x' AAN naar wat je bij stap 1 zag!
# venv_path = project_root / ".venv" / "lib" / "python3.12" / "site-packages"

# # Voeg het pad toe aan de Python zoeklijst
# sys.path.insert(0, str(venv_path))

# # TEST DE IMPORT
# try:
#     from mlx import Mlx
#     print("✅ Succes: Mlx is geladen!")
#     # Hier kun je je code verder schrijven:
#     # engine = Mlx()
# except ImportError as e:
#     print(f"❌ Fout: Kon 'mlx' niet vinden in {venv_path}")
#     print(f"Details: {e}")