from tests import Maze, ConfigError, ConfigParser
from tests import ExitCell, EntryCell, FourtyTwoCell
import mlx
from tests import MlxContext, ImageBuffer, MazeRenderer
from tests import (write_hexadecimal_map_to_file,
                   convert_cell_path_to_directions)
from tests import SinglePathSolver, ShortestPathSolver
from tests import loop_handler, exit_loop, key_handler_factory
import sys
# import time

# Pick a seed, just a random number, fill in the config file in project.
# Then generate the maze from the project folder by runnning it with:
# python3 -m tests.test_maze config.txt
frame = 0


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
    seed = config["seed"]

    maze = Maze(maze_width, maze_height, seed)

    maze.place_fourty_two_glyph_at_maze_center()
    maze.place_entry_and_exit_cells(config["entry"], config["exit"])
    if config["perfect"] is True:
        maze.generate_perfect_maze()
        perfect_solver = SinglePathSolver(maze)
        solution = perfect_solver.solve()
    elif config["perfect"] is False:
        maze.generate_simple_maze()
        short_path_solver = ShortestPathSolver(maze)
        solution = short_path_solver.solve()

    # print(solution, len(solution))

    for path in solution:
        path_for_file = path

    write_hexadecimal_map_to_file(maze, config["entry"], config["exit"],
                                  path_for_file,
                                  config["output_file"]
                                  )

    directions = convert_cell_path_to_directions(maze, path_for_file)
    print(directions, len(directions))
    sol_path = [(c, d) for c, d in zip(solution[0][1:-1],directions[1:])]
    print(sol_path, len(sol_path))

    default_options = {"MUSIC_FILE": True,
                       "COLOR_WALLS": 0xFF00AAAA,
                       "COLOR_BACKGROUND": 0xFF2200FF,
                       "COLOR_FOURTYTWO": 0xFFFFFFFF,
                       "COLOR_ENTRY": 0xFFFF00FF,
                       "COLOR_EXIT": 0xFF00FF00,
                       "COLOR_MENUTEXT": 0xFF0000,
                       "CELL_SIZE": 60,
                       "PERC_WALL": 0.2,
                       "PERC_PADDING": 0.2}

    context = MlxContext(mlx.Mlx())
    if config["cell_size"]:
        cell_size = config["cell_size"]
    else:
        cell_size = default_options["CELL_SIZE"]

    if config["perc_wall"]:
        perc_wall = config["perc_wall"]
    else:
        perc_wall = default_options["PERC_WALL"]

    if config["perc_padding"]:
        perc_pad = config["perc_padding"]
    else:
        perc_pad = default_options["PERC_PADDING"]

    # important, but precalculated in advance...
    img_width = ((cell_size * maze_width) - (
        (maze_width - 1) * int(cell_size * perc_wall)))

    # important, but precalculated in advance...
    img_height = ((cell_size * maze_height) - (
        (maze_height - 1) * int(cell_size * perc_wall)))

    viewport = context.create_new_viewport(img_width, img_height, "maze test")
    image = context.create_new_image(ImageBuffer, img_width, img_height)

    # image.clear()
    renderer = MazeRenderer(cell_size, perc_wall, perc_pad)
    # renderer.draw(image, maze.two_dimensional_cell_grid)
    # viewport.add_img(image)

    if config["color_background"]:
        color_background = config["color_background"]
    else:
        color_background = default_options["COLOR_BACKGROUND"]
    if config["color_fourtytwo"]:
        color_fourtytwo = config["color_fourtytwo"]
    else:
        color_fourtytwo = default_options["COLOR_FOURTYTWO"]
    if config["color_walls"]:
        color_walls = config["color_walls"]
    else:
        color_walls = default_options["COLOR_WALLS"]
    if config["color_entry"]:
        color_entry = config["color_entry"]
    else:
        color_entry = default_options["COLOR_ENTRY"]
    if config["color_exit"]:
        color_exit = default_options["COLOR_EXIT"]
    else:
        color_exit = default_options["COLOR_EXIT"]

    renderer.renderer_queue = ["background", "walls", "doors", "path"]
    renderer.animations = {
        "globals": {
            "frame_count": 0
        },
        "elements": {
            "background": {
                "target": maze.two_dimensional_cell_grid,
                "color": color_background
            },
            "fourtytwo": {
                "target": [cell for rows in maze.two_dimensional_cell_grid
                           for cell in rows
                           if isinstance(cell, FourtyTwoCell)],
                "in_color": color_fourtytwo
            },
            "walls": {
                "target": (cell for rows in maze.two_dimensional_cell_grid
                           for cell in rows),
                "color": color_walls
            },
            "entry": {
                "target": [cell for rows in maze.two_dimensional_cell_grid
                           for cell in rows if isinstance(cell, EntryCell)],
                "in_color": color_entry
            },
            "exit": {
                "target": [cell for rows in maze.two_dimensional_cell_grid
                           for cell in rows if isinstance(cell, ExitCell)],
                "in_color": color_exit
            },
            "path": {
                "target": (state for state in sol_path),
                "in_color": 0xFFDDDDDD,
                "on": True
            }
        }}

    # time.sleep(2)

    # event hooks
    context.mlxbinding.mlx_hook(viewport.viewport_ptr,
                                33, 0,
                                exit_loop,
                                context.mlx_ptr)
    context.mlxbinding.mlx_key_hook(viewport.viewport_ptr,
                                    key_handler_factory,
                                    [context, viewport, image, renderer,
                                     sol_path])
    context.mlxbinding.mlx_loop_hook(context.mlx_ptr,
                                     loop_handler,
                                     [context, viewport, image, renderer])

    if config["color_menutext"]:
        color_menutext = config["color_menutext"]
    else:
        color_menutext = default_options["COLOR_MENUTEXT"]

    help_vp = context.create_new_viewport(300, 200, "Controls")
    help_vp.string_put(20, 30, color_menutext, " ---__\\.CONTROLS./__---")
    help_vp.string_put(20, 60, color_menutext,
                       "ESC:\tExit program".expandtabs(8))  # TODO
    help_vp.string_put(20, 90, color_menutext,
                       "r:\tReload Maze".expandtabs(8))
    # help_vp.string_put(20, 120, color_menutext,
    #                    "m:\tSolve".expandtabs(8))
    help_vp.string_put(20, 120, color_menutext,
                       "p:\tHide/Show Path".expandtabs(8))
    context.start_loop()
    context.destroy_viewport(help_vp.viewport_ptr)
    context.destroy_viewport(viewport.viewport_ptr)


if __name__ == "__main__":
    main()
