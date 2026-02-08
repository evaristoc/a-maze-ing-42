from tests import Maze, ConfigError, ConfigParser
import mlx
from tests import MlxContext, Canvas, MlxImageBuffer, MazeRenderer
from tests import write_hexadecimal_map_to_file
import sys

# Pick a seed, just a random number, fill in the config file in project.
# Then generate the maze from the project folder by runnning it with:
# python3 -m tests.test_maze config.txt


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
    seed = 122

    maze = Maze(maze_width, maze_height, seed)

    maze.place_fourty_two_glyph_at_maze_center()
    maze.place_entry_and_exit_cells(config["entry"], config["exit"])
    if config["perfect"] is True:
        maze.generate_perfect_maze()
    elif config["perfect"] is False:
        maze.generate_simple_maze()

    # maze.randomly_remove_some_walls(0.6)
    context = MlxContext(mlx.Mlx())
    print(context)
    cell_size = 7
    canvas = context.create_new_canvas(maze_width*cell_size, maze_height*cell_size, "maze")
    print(canvas)

    #image = context.create_new_image(maze_width, maze_height)
    image = conntext.create_new_image(MlxImageBuffer, maze_width*cell_size, maze_height*cell_size)
    print(image)
    image.clear()

    renderer = MazeRenderer(cell_size)
    print(renderer)

    print(maze.two_dimensional_cell_grid)

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
