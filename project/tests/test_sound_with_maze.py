from tests import Maze, ConfigError, ConfigParser
import mlx
from tests import MlxContext, ImageBuffer, MazeRenderer
from tests import write_hexadecimal_map_to_file
from tests import SinglePathSolver
import sys
from time import sleep
import pygame
from tests import SoundManager

pygame.init()


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
    # print(solution)

    for path in solution:
        path_for_file = path

    write_hexadecimal_map_to_file(maze, config["entry"], config["exit"],
                                  path_for_file,
                                  config["output_file"]
                                  )

    # Create sound_manager
    sound_manager = SoundManager()

    # Load sounds
    sound_manager.load_sound("bell_l",
                             "sound_effects/bell_large.mp3")
    sound_manager.load_sound("bell_m",
                             "sound_effects/bell_medium.mp3")
    sound_manager.load_sound("sunscreen",
                             "sound_effects/sunscreen_rub.mp3")
    sound_manager.load_sound("wooden_clacker",
                             "sound_effects/wooden_clacker.mp3")
    sound_manager.load_music("music/de_basis_samone.mp3")

    context = MlxContext(mlx.Mlx())
    cell_size = 60
    img_width = cell_size * maze_width - (maze_width - 1) * int(cell_size * .2) # important, but precalculated in advance...
    img_height = cell_size * maze_height - (maze_height - 1) * int(cell_size * .2) # important, but precalculated in advance...
    viewport = context.create_new_viewport(img_width, img_height, "maze test")
    image = context.create_new_image(ImageBuffer, img_width, img_height)
    #image.clear()
    renderer = MazeRenderer(cell_size)
    renderer.draw(image, maze.two_dimensional_cell_grid)
    viewport.add_img(image)
    def gere_close_1(context):
        try:
            print("Exiting the mlx loop...")
            context.mlxbinding.mlx_loop_exit(context.mlx_ptr)
        except Exception as e:
            print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
            sys.exit(1) 
    context.mlxbinding.mlx_hook(viewport.viewport_ptr, 33, 0, gere_close_1, context)
    sound_manager.play_sound("sunscreen")
    sleep(1)
    sound_manager.play_music()
    context.start_loop()
    context.destroy_window(viewport.viewport_ptr)
    sound_manager.stop_music()
    sound_manager.play_sound("wooden_clacker")
    sleep(0.5)
    sound_manager.play_sound("bell_m")
    sleep(0.5)
    sound_manager.play_sound("bell_l")
    sleep(3)


if __name__ == "__main__":
    main()
