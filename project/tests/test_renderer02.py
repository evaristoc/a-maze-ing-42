from tests import Maze, ConfigError, ConfigParser
import mlx
from tests import MlxContext, Canvas, MlxImageBuffer, MazeRenderer
from tests import write_hexadecimal_map_to_file
import sys

# Pick a seed, just a random number, fill in the config file in project.
# Then generate the maze from the project folder by runnning it with:
# python3 -m tests.test_maze config.txt

class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0

class XVar:
    """Structure for main vars"""
    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.win_1 = None
        self.win_2 = None
        self.img_1 = ImgData()
        self.img_2 = ImgData()
        self.img_png = ImgData()
        self.img_xpm = ImgData()
        self.imgidx = 0


def main() -> None:
    xvar = XVar()

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
    xvar.mlx = MlxContext(mlx.Mlx())
    print(xvar.mlx)
    xvar.mlx_ptr = xvar.mlx.mlx_ptr
    print(xvar.mlx_ptr)
    print(xvar.mlx.mlx.mlx_get_screen_size(xvar.mlx_ptr))
    # xvar.win_1 = xvar.mlx._create_new_canvas(400, 400, "test")
    xvar.win_1 = xvar.mlx.mlx.mlx_new_window(xvar.mlx_ptr, 400, 400, "test")
    xvar.img_1.img = xvar.mlx.mlx.mlx_new_image(xvar.mlx_ptr, 200, 200)
    xvar.img_1.width = 200
    xvar.img_1.height = 200
    xvar.img_1.data, xvar.img_1.bpp, xvar.img_1.sl, xvar.img_1.iformat = \
        xvar.mlx.mlx.mlx_get_data_addr(xvar.img_1.img)
    # Fill image #1
    for i in range(xvar.img_1.sl * 200):
        xvar.img_1.data[i] = 0x80

    for i in range(xvar.img_1.sl * 100):
        xvar.img_1.data[i] = 0xFF

    try:
        # Add some red pixels
        pixel_positions = [
            0 * 200 * 4,                   # top left
            (1 * 200 + 1) * 4,             # top left + 1
            (199 * 200 + 199) * 4,         # bottom right
            (198 * 200 + 198) * 4          # bottom right - 1
        ]
        
        for pos in pixel_positions:
            if pos < len(xvar.img_1.data) - 3:
                xvar.img_1.data[pos:pos+4] = (0xFFFF0000).to_bytes(4, 'little')
    except Exception as e:
        print(f"Error img1: {e}", file=sys.stderr)
        sys.exit(1)

    def gere_close_1(xvar):
        xvar.mlx.mlx.mlx_loop_exit(xvar.mlx_ptr)
    xvar.mlx.mlx.mlx_hook(xvar.win_1, 33, 0, gere_close_1, xvar)

    xvar.mlx.mlx.mlx_loop(xvar.mlx_ptr)
    xvar.mlx.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)

    # cell_size = 25
    # canvas = Canvas(context, maze_width * cell_size, maze_height * cell_size, "maze test")
    #this is incorrect!!!
    #canvas_idptr = context.create_new_canvas(maze_width*cell_size, maze_height*cell_size, "maze")
    # print(canvas)

    # #image = context.create_new_image(maze_width, maze_height)
    # image = canvas.create_new_image(MlxImageBuffer, maze_width*cell_size, maze_height*cell_size)
    # print(image)
    # image.clear()
    # # print("bpp",image.bytes_per_pixel)
    # renderer = MazeRenderer(cell_size)
    # print(renderer)
    # renderer.draw(image, maze.two_dimensional_cell_grid)
    # canvas.present(image)

    # #print(maze.two_dimensional_cell_grid[0][0])
    # def gere_close_1(context):
    #     context.mlx.mlx_loop_exit(context.mlx_ptr)
    # context.mlx.mlx_hook(canvas._win, 33, 0, gere_close_1, context) 
    # context.create_loop()
    # context.destroy_window(canvas._win)



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
