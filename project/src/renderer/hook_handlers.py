import mlx
from typing import Type
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
config_path = os.path.join(project_root, "config.txt")

def loop_handler(params: list) -> None:
    context, viewport, renderer = params
    if not renderer.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(context.img_asset)
        return
    renderer.animations["globals"]["frame_count"] += 1
    if renderer.animations["globals"]["frame_count"] % 1 != 0:
        viewport.add_img(context.img_asset)
        return 0
    if renderer.renderer_queue[0] == "background":
        renderer.draw(context.img_asset, renderer.animations["elements"]["background"]["target"],  {"background":renderer.animations["elements"]["background"]["color"]})
        renderer.draw(context.img_asset, [renderer.animations["elements"]["fourtytwo"]["target"]], {"fourtytwo":renderer.animations["elements"]["fourtytwo"]["in_color"]})
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(renderer.animations["elements"]["walls"]["target"], None)
        if current is not None:
            renderer.draw(context.img_asset, [[current]], {"walls":renderer.animations["elements"]["walls"]["color"]})
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(context.img_asset, [renderer.animations["elements"]["exit"]["target"]], {"exit": renderer.animations["elements"]["exit"]["in_color"]})
        renderer.draw(context.img_asset, [renderer.animations["elements"]["entry"]["target"]], {"entrance": renderer.animations["elements"]["entry"]["in_color"]})
        renderer.renderer_queue.pop(0)
    viewport.add_img(context.img_asset)
    return 0

def close_viewport_handler(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
        sys.exit(1)

def update(params: list)
    context, viewport, renderer = params
    try:
        config = ConfigParser.from_file(config_path)
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

    cell_size = 60
    img_width = cell_size * maze_width - (maze_width - 1) * int(cell_size * .2) # important, but precalculated in advance...
    img_height = cell_size * maze_height - (maze_height - 1) * int(cell_size * .2) # important, but precalculated in advance...
    context.destroy_image(context.img_asset.img_ptr)
    context.destroy_viewport(viewport.viewport_ptr)
    viewport = context.create_new_viewport(img_width, img_height, "maze test")
    context.create_new_image(ImageBuffer, img_width, img_height)
    renderer.renderer_queue = ["background", "walls", "doors"]
    renderer.animations["globals"]["frame_count"] = 0
    time.sleep(2)
    context.mlxbinding.mlx_key_hook(viewport.viewport_ptr, reload_handler, [context, viewport, renderer])
    context.mlxbinding.mlx_hook(viewport.viewport_ptr, 33, 0, close_viewport_handler, context.mlx_ptr)
    context.mlxbinding.mlx_loop_hook(context.mlx_ptr, loop_handler, [context, viewport, renderer])
    return

def reload_handler(key: int, params: list) -> int:
    # params: [context, viewport, renderer]
    
    # 1. ESC to Close (Safety)
    if keycode == 65307: # ESC key
        # Call your close logic
        return 0

    # 2. 'R' to Reload
    if keycode == 114: # 'r' key
        print("Reloading...")
        update(params)
        
    return 0

