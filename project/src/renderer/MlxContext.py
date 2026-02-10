from .Viewport import Viewport
from .Image import Image

class MlxContext:
    """
    mlx_binding == mlx.Mlx() -- wrapper instance, binding to MiniLibX backend
    mlxbinding.mlx == mlxbackend
    mlxbinding.mlx.mlx_ptr == mlx_ptr (pointer to the running MiniLibX backend)
    """"
    def __init__(self, mlx_binding: Mlx) -> None:
        try:
            # the minilibx is instantiated
            self._mlxbinding = mlx_binding
            # the pointer is instantiated
            self._mlx_ptr = self._mlxbinding.mlx_init()
            if not self._mlx_ptr:
                raise RuntimeError("mlx_init() failed to return a pointer")
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)

    @property
    def mlxbinding(self) -> any:
        return self._mlxbinding

    @property
    def mlxbackend(self) -> any:
        return self._mlxbinding.mlx
    
    @property
    def mlx_ptr(self) -> any:
        return self._mlx_ptr

    def get_size(self) -> tuple:
        return self.mlxbackend.get_screen_size(self.mlx_ptr)

    def create_new_viewport(self, w: int, h: int, title: str) -> any:
        viewport = Viewport()
        try:
            viewport.viewport_ptr = self.mlxbackend.mlx_new_window(
                self.mlx_ptr,
                w,
                h,
                title)
            viewport.height = h
            viewport.width = w
            viewport.title = title
            viewport.context = self._mlxbinding #to add to viewport the ability to eventually add images
             if not viewport.viewport_ptr:
                raise Exception(f"Can't create {title} viewport")
        except Exception as e:
            print(f"Error: viewport raised: {e}", file=sys.stderr)
            sys.exit(1)
        return viewport

    def create_new_image(self, Img_Class: Image, w: int, h: int) -> Image:
        img = Img_Class()
        img.img_ptr = self.mlxbackend.mlx_new_image(self.mlx_ptr, w, h)
        #TODO error handing
        img.width = w
        img.height = h
        img.data, img.bytes_per_pixel, img.stride, img.endian = \
        self.mlxbackend.mlx_get_data_addr(img.img_ptr)
        return img
    
    def start_loop(self):
        self.mlxbackend.mlx_loop(self.mlx_ptr)

    def destroy_window(self, viewport_ptr: any):
        self.mlxbackend.mlx_destroy_window(self.mlx_ptr, viewport_ptr)
    
    def destroy_image():
        #TODO
        pass