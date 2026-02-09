from .Image import Image

class MlxContext:
    def __init__(self, mlx_lib: any) -> None:
        try:
            # the minilibx is instantiated
            self.mlx = mlx_lib
            # the pointer is instantiated
            self.mlx_ptr = self.mlx.mlx_init()
            if not self.mlx_ptr:
                raise RuntimeError("mlx_init() failed to return a pointer")
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)

    def get_mlx_ptr(self) -> any:
        return self.mlx_ptr

    def get_size(self) -> tuple:
        return self.mlx.get_screen_size(self.mlx_ptr)

    def _create_new_canvas(self, w: int, h: int, title: str) -> any:
        return self.mlx.mlx_new_window(self.mlx_ptr, w, h, title)

    # def _create_new_image(self, img_class: Image, w: int, h: int) -> Image:
    #     img = img_class()
    #     img.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, w, h)
    #     #TODO error handing
    #     img.width = w
    #     img.height = h
    #     img.data, img.bytes_per_pixel, img.stride, img.endian = \
    #     self.mlx.mlx_get_data_addr(img.img_ptr)
    #     return img
    
    def create_loop(self):
        self.mlx.mlx_loop(self.mlx_ptr)

    def destroy_window(self, canvas: any):
        self.mlx.mlx_destroy_window(self.mlx_ptr, canvas)
    
    def destroy_image():
        #TODO
        pass