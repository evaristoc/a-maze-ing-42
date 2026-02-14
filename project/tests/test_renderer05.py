from tests import Maze, ConfigError, ConfigParser
from tests import (Cell, ExitCell, EntryCell, FourtyTwoCell)
import mlx
from tests import MlxContext, ImageBuffer, MazeRenderer
from tests import write_hexadecimal_map_to_file, convert_cell_path_to_directions
from tests import SinglePathSolver
from tests import loop_handler, reload_handler, close_viewport_handler
import sys
import time

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
    seed = 122

    maze = Maze(maze_width, maze_height, seed)

    maze.place_fourty_two_glyph_at_maze_center()
    maze.place_entry_and_exit_cells(config["entry"], config["exit"])
    if config["perfect"] is True:
        maze.generate_perfect_maze()
    elif config["perfect"] is False:
        maze.generate_simple_maze()

    # maze.randomly_remove_some_walls(0.6)
    perfect_solver = SinglePathSolver(maze)
    solution = perfect_solver.solve()
    print(solution)
    
    for path in solution:
        path_for_file = path

    path = convert_cell_path_to_directions(maze, path_for_file)
    print(path)
    
    # maze.randomly_remove_some_walls(0.6)
    context = MlxContext(mlx.Mlx())
    cell_size = 60
    img_width = cell_size * maze_width - (maze_width - 1) * int(cell_size * .2) # important, but precalculated in advance...
    img_height = cell_size * maze_height - (maze_height - 1) * int(cell_size * .2) # important, but precalculated in advance...
    viewport = context.create_new_viewport(img_width, img_height, "maze test")
    image = context.create_new_image(ImageBuffer, img_width, img_height)
    #image.clear()
    renderer = MazeRenderer(cell_size)
    #renderer.draw(image, maze.two_dimensional_cell_grid)
    #viewport.add_img(image)
    renderer.renderer_queue = ["background", "walls", "doors"]
    renderer.animations = {
        "globals":{
            "frame_count": 0
        },
        "elements":{
            "background":{
                "target": maze.two_dimensional_cell_grid,
                "color": 0xFF2200FF
            },
            "fourtytwo":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, FourtyTwoCell)],
                "in_color": 0xFFFFFFFF
            },
            "walls":{
                "target": (cell for rows in maze.two_dimensional_cell_grid for cell in rows),
                "color": 0xFF00AAAA
            },
            "entry":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, EntryCell)],
                "in_color": 0xFFFF00FF
            },
            "exit":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, ExitCell)],
                "in_color": 0xFF00FF00
            },
        }}
        
    time.sleep(2)

    # event hooks
    context.mlxbinding.mlx_key_hook(viewport.viewport_ptr, reload_handler, [context, viewport, image, renderer])
    context.mlxbinding.mlx_hook(viewport.viewport_ptr, 33, 0, close_viewport_handler, context.mlx_ptr)
    context.mlxbinding.mlx_loop_hook(context.mlx_ptr, loop_handler, [context, viewport, image, renderer])
    help_vp = context.create_new_viewport(300, 200, "Controls")
    help_vp.string_put(20, 30, 0xFFFFFF, "CONTROLS")
    help_vp.string_put(20, 60, 0xFFFFFF, "R: Reload Maze")
    help_vp.string_put(20, 90, 0xFFFFFF, "M: Solve")
    context.start_loop()
    context.destroy_viewport(help_vp.viewport_ptr)
    context.destroy_viewport(viewport.viewport_ptr)

if __name__ == "__main__":
    main()