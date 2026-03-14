import sys
import mlx
from mazegen import ExitCell, EntryCell, FourtyTwoCell
from mazegen import MazeGenerator
from collect_config_variables.error_handlers.config_errors import (
    ConfigError)
from src import (MlxContext, AppResources, RasterImage,
                 ConfigParser, ImageBuffer, MazeRenderer)
from src import loop_handler, exit_loop_handler, key_handler_controller, mouse_event
from time import sleep
from src.sound_effects_and_music import SoundManager
import pygame  # noqa E402
RD = "\033[91m"
R = "\033[0m"

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


def render_maze(params: AppResources) -> None:
    # context, viewport, image, renderer,
    # sol_path, update, configurationfile, ui = params
    try:
        config = ConfigParser.from_file(params.config_file)
        config = config.config_parser_output_into_dict(config)
    except ConfigError as error:
        print(f"Error:\t{error}")
        sound_man = SoundManager()
        sound_man.load_sound("bell", "sound_effects/bell_medium.mp3")
        sound_man.play_sound("bell")
        sleep(0.8)
        return
    maze_width = config["width"]
    maze_height = config["height"]
    seed = config["seed"]

    # ============================================
    # ======= MazeGenerator start ================
    maze_generator = MazeGenerator(maze_width, maze_height, seed)

    maze_generator.generate(
        perfect=config["perfect"],
        entry=config["entry"],
        exit=config["exit"]
    )

    maze = maze_generator.maze  # preserve original behavior
    sol_path = maze_generator.get_directions()

    maze_generator.save(config["output_file"])

    # ============================================
    # ======= MazeGenerator ends =================

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

    if params.image:
        params.context.destroy_image(params.image.img_ptr)
    if params.viewport:
        params.context.destroy_viewport(params.viewport.viewport_ptr)

    # important, but precalculated in advance...
    img_width = ((cell_size * maze_width) - (
        (maze_width - 1) * int(cell_size * perc_wall)))

    tot_img_width = max(img_width, params.buttons['reload'].width) # hardcoding legend width

    # important, but precalculated in advance...
    img_height = ((cell_size * maze_height) - (
        (maze_height - 1) * int(cell_size * perc_wall)))


    tot_img_height = img_height  + 4 * params.buttons['reload'].height + 15 # hardcoding legend height

    params.viewport = params.context.create_new_viewport(
        tot_img_width,
        tot_img_height,
        "MAZE" # TODO: this can be dynamically changed
    )
    params.image = params.context.create_new_image(
        ImageBuffer,
        img_width,
        img_height
    )

    params.renderer = MazeRenderer(cell_size, perc_wall, perc_pad)

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

    params.renderer.renderer_queue = ["background", "walls", "doors", "path"]
    params.renderer.animations = {
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
                "target_all": [cell for rows in maze.two_dimensional_cell_grid
                               for cell in rows],
                "color": color_walls,
                "on": True
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
                "target_all": sol_path,
                "in_color": 0xFFDDDDDD,
                "on": True
            }
        }}

    if not params.ui_viewport:
        if config["color_menutext"]:
            color_menutext = config["color_menutext"]
        else:
            color_menutext = default_options["COLOR_MENUTEXT"]
        params.ui_viewport = params.context.create_new_viewport(
            300,
            200,
            "Controls"
        )
        params.ui_viewport.string_put(20, 30, color_menutext,
                                      " ---__\\.CONTROLS./__---")
        params.ui_viewport.string_put(20, 60, color_menutext,
                                      "ESC:\tExit program".expandtabs(8))
        params.ui_viewport.string_put(20, 90, color_menutext,
                                      "r:\tReload Maze".expandtabs(8))
        params.ui_viewport.string_put(20, 120, color_menutext,
                                      "p:\tHide/Show Path".expandtabs(8))
        params.ui_viewport.string_put(20, 150, color_menutext,
                                      "w:\tWalls Colors".expandtabs(8))
    # event hooks
    params.context.mlxbinding.mlx_hook(params.viewport.viewport_ptr,
                                       33, 0,
                                       exit_loop_handler,
                                       params.context.mlx_ptr)
    params.context.mlxbinding.mlx_mouse_hook(params.viewport.viewport_ptr,
                                        mouse_event,
                                        params
                                        )
    params.context.mlxbinding.mlx_key_hook(params.viewport.viewport_ptr,
                                           key_handler_controller,
                                           params)
    params.context.mlxbinding.mlx_loop_hook(params.context.mlx_ptr,
                                            loop_handler,
                                            [
                                                params.viewport,
                                                params.image,
                                                params.renderer,
                                                params.buttons
                                            ])


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:\tpython main.py <config_file>")
        return
    try:
        config = ConfigParser.from_file(sys.argv[1])
        config = config.config_parser_output_into_dict(config)
    except ConfigError as error:
        print(f"{RD}Error:\t{error}{R}")
        sound_man = SoundManager()
        sound_man.load_sound("bell_large", "sound_effects/bell_large.mp3")
        sound_man.play_sound("bell_large")
        sleep(0.8)
        return
    config_file = sys.argv[1]
    context = MlxContext(mlx.Mlx())
    params = AppResources()
    params.context = context
    params.update_func = render_maze
    params.config_file = config_file
    if not params.buttons:
        params.buttons = dict()
        params.buttons["esc"] = context.load_image("assets/esc.png")
        params.buttons["reload"] = context.load_image("assets/reload.png")
        params.buttons["walls"] = context.load_image("assets/walls.png")
        params.buttons["path"] = context.load_image("assets/path.png")     
    render_maze(params)
    sound_man = SoundManager()
    sound_man.load_music("music/de_basis_samone.mp3")
    sound_man.play_music()
    context.start_loop()
    # current_ui_vp
    if params.ui_viewport:
        context.destroy_viewport(params.ui_viewport.viewport_ptr)
    # current_vp
    if params.viewport:
        context.destroy_viewport(params.viewport.viewport_ptr)
    sound_man.stop_music()
    sound_man.load_sound("bell_medium", "sound_effects/bell_medium.mp3")
    sound_man.play_sound("bell_medium")
    sleep(1)


if __name__ == "__main__":
    main()
