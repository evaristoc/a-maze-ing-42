from tests import Maze, ConfigError, ConfigParser
#from src.collect_config_variables import ConfigParser
import sys

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
        # self.win_2 = None
        self.img_1 = ImgData()
        # self.img_2 = ImgData()
        # self.img_png = ImgData()
        # self.img_xpm = ImgData()
        self.imgidx = 0

# To place a pixel at (x, y), we use the 'sl' (bytes per line)
    def put_pixel(img, x, y, r, g, b):
        # Offset = (y * bytes_per_line) + (x * bytes_per_pixel)
        # Assuming 32-bit (4 bytes per pixel)
        pos = (y * img.sl) + (x * (img.bpp // 8))
        if pos < len(img.data) - 4:
            # Most X11 systems use BGRA (Little Endian)
            img.data[pos] = b      # Blue
            img.data[pos + 1] = g  # Green
            img.data[pos + 2] = r  # Red
            img.data[pos + 3] = 0  # Alpha/Transparency

def gere_close(xvar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
    sys.exit(0)

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
    xvar = XVar()
	# TEST DE IMPORT
    try:
        from mlx import Mlx
        print("✅ Succes: Mlx is geladen!")
        # Hier kun je je code verder schrijven:
    except ImportError as e:
        print(f"❌ Fout: Kon 'mlx' niet vinden in {venv_path}")
        print(f"Details: {e}")
    # Mlx Initialisation
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)
    xvar.mlx_ptr = xvar.mlx.mlx_init()
    try:
        xvar.win_1 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, 400, 400, "MLX main win")
        if not xvar.win_1:
            raise Exception("Can't create main window")
        # xvar.win_2 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, 150, 150, "Secondary window")
        # if not xvar.win_2:
        #     raise Exception("Can't create secondary window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)
    # Image #1
    xvar.img_1.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, 200, 200)
    if not xvar.img_1.img:
        raise Exception("Can't create image 1")           
    xvar.img_1.width = 200
    xvar.img_1.height = 200
    xvar.img_1.data, xvar.img_1.bpp, xvar.img_1.sl, xvar.img_1.iformat = \
        xvar.mlx.mlx_get_data_addr(xvar.img_1.img)
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
    xvar.mlx.mlx_hook(xvar.win_1, 17, 0, gere_close, xvar)
    try:
        xvar.mlx.mlx_loop(xvar.mlx_ptr)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        if xvar.win_1:
            xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)
        if xvar.img_1.img:
            xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.img_1.img)
        print("Memory Handshake: Local resources freed.")
        sys.exit(0)       

    # win_ptr = xvar.mlx.mlx_new_window(mlx_ptr, maze_width*10, maze_height*10, "win title")
    # xvar.mlx.mlx_clear_window(mlx_ptr, win_ptr)
    # xvar.mlx.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
    # (ret, w, h) = xvar.mlx.mlx_get_screen_size(mlx_ptr)
    # xvar.mlx.mlx_hook(xvar.win_1, 17, 0, gere_close, xvar)
    # xvar.mlx.mlx_loop(mlx_ptr)
    # xvar.mlx.mlx_clear_window(mlx_ptr, win_ptr)
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