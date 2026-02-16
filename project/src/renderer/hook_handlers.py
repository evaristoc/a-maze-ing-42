import mlx
from typing import Type
import os
from src.collect_config_variables.config_parser import ConfigParser
from src.renderer.Image import ImageBuffer
from src.collect_config_variables.error_handlers.config_errors import ConfigError
from src.maze_factory.maze import Maze
from src.maze_factory.cells import Cell, ExitCell, EntryCell, FourtyTwoCell
from src.renderer import MazeRenderer
#from tests import (Cell, ExitCell, EntryCell, FourtyTwoCell)
#import mlx
#from tests import MlxContext, ImageBuffer, MazeRenderer
from src.map import write_hexadecimal_map_to_file, convert_cell_path_to_directions
from src.maze_solvers.single_path_solver import SinglePathSolver
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
config_path = os.path.join(project_root, "config.txt")

def loop_handler(params: list) -> None:
    context, viewport, img, renderer = params
    if not renderer.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(img)
        return
    renderer.animations["globals"]["frame_count"] += 1
    if renderer.animations["globals"]["frame_count"] % 1 != 0:
        viewport.add_img(img)
        return 0
    if renderer.renderer_queue[0] == "background":
        renderer.draw(img, renderer.animations["elements"]["background"]["target"],  {"background":renderer.animations["elements"]["background"]["color"]})
        renderer.draw(img, [renderer.animations["elements"]["fourtytwo"]["target"]], {"fourtytwo":renderer.animations["elements"]["fourtytwo"]["in_color"]})
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(renderer.animations["elements"]["walls"]["target"], None)
        if current is not None:
            renderer.draw(img, [[current]], {"walls":renderer.animations["elements"]["walls"]["color"]})
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(img, [renderer.animations["elements"]["exit"]["target"]], {"exit": renderer.animations["elements"]["exit"]["in_color"]})
        renderer.draw(img, [renderer.animations["elements"]["entry"]["target"]], {"entrance": renderer.animations["elements"]["entry"]["in_color"]})
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "path":
        current = next(renderer.animations["elements"]["path"]["target"], None)
        if current is not None:
            renderer.draw(img, [[current]], {"path": renderer.animations["elements"]["path"]["in_color"]})
        else:
            renderer.renderer_queue.pop(0)
    viewport.add_img(img)
    return 0

def exit_loop(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
        sys.exit(1)

def update(params: list) -> None:
    context, viewport, img, renderer, _ = params
    print("Reloading...")
    try:
        config = ConfigParser.from_file(config_path)
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
    elif config["perfect"] is False:
        maze.generate_simple_maze()

    # maze.randomly_remove_some_walls(0.6)
    perfect_solver = SinglePathSolver(maze)
    solution = perfect_solver.solve()
    print(solution)

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

    img_width = cell_size * maze_width - (maze_width - 1) * int(cell_size * perc_wall) # important, but precalculated in advance...
    img_height = cell_size * maze_height - (maze_height - 1) * int(cell_size * perc_wall) # important, but precalculated in advance...
    context.destroy_image(img.img_ptr)
    context.destroy_viewport(viewport.viewport_ptr)
    viewport = context.create_new_viewport(img_width, img_height, "maze test")
    img = context.create_new_image(ImageBuffer, img_width, img_height)

    renderer = MazeRenderer(cell_size, perc_wall, perc_pad)


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
        "globals":{
            "frame_count": 0
        },
        "elements":{
            "background":{
                "target": maze.two_dimensional_cell_grid,
                "color": color_background
            },
            "fourtytwo":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, FourtyTwoCell)],
                "in_color": color_fourtytwo
            },
            "walls":{
                "target": (cell for rows in maze.two_dimensional_cell_grid for cell in rows),
                "color": color_walls
            },
            "entry":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, EntryCell)],
                "in_color": color_entry
            },
            "exit":{
                "target": [cell for rows in maze.two_dimensional_cell_grid for cell in rows if isinstance(cell, ExitCell)],
                "in_color": color_exit
            },
            "path": {
                "target": (state for state in sol_path),
                "in_color": 0xFFDDDDDD,
                "on": True
            }            
        }}
    context.mlxbinding.mlx_hook(viewport.viewport_ptr, 33, 0, exit_loop, context.mlx_ptr)
    context.mlxbinding.mlx_key_hook(viewport.viewport_ptr, key_factory_handler, [context, viewport, img, renderer, sol_path])
    context.mlxbinding.mlx_loop_hook(context.mlx_ptr, loop_handler, [context, viewport, img, renderer])
    return
    
def vis_path(params: list) -> int:
    # params: [viewport, img, renderer, state]
    _, viewport, img, renderer, state = params
    print("Path handling...")
    if not renderer.animations["elements"]["path"]["on"]:
        for c, d in state:
            renderer.draw(img, [[(c, d)]], {"path": renderer.animations["elements"]["path"]["in_color"]})
            renderer.animations["elements"]["path"]["on"] = True
    else:
        for c, d in state:
            print(c, d)
            renderer.draw(img, [[(c, d)]], {"path": renderer.animations["elements"]["background"]["color"]})
            renderer.animations["elements"]["path"]["on"] = False
    viewport.add_img(img)         
    return

def key_handler_factory(keycode: int, params: list) -> int:
    # params: [context, viewport, img, renderer, state]
    if keycode == 65307: # ESC key
        exit_loop(params[0].mlx_ptr)
        return 0
    if keycode == 112: # 'p' key
        vis_path(params)
    if keycode == 114: # 'r' key
        update(params)
        
    return 0