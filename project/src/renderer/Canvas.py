import sys
from .MlxContext import MlxContext
from .Image import Image

class Canvas:
    def __init__(self, context: MlxContext, w: int, h: int, title: str) -> None:
        self.context = context
        try:
            self._win = self.context._create_new_canvas(w, h, title)
            if not self._win:
                raise Exception(f"Can't create {title} window")
        except Exception as e:
            print(f"Error: Win create: {e}", file=sys.stderr)
            sys.exit(1)
        #self.main_buffer = Image()
        self.main_buffer = None

    def create_new_image(self, img_class: Image, w: int, h: int) -> Image:
        self.main_buffer = img_class()
        self.main_buffer.img_ptr = self.context.mlx.mlx_new_image(self.context.mlx_ptr, w, h)
        #TODO error handing
        self.main_buffer.width = w
        self.main_buffer.height = h
        self.main_buffer.data, self.main_buffer.bytes_per_pixel, self.main_buffer.stride, self.main_buffer.endian = \
        self.context.mlx.mlx_get_data_addr(self.main_buffer.img_ptr)
        return self.main_buffer

    ## for buffering a single, modifiable image
    def present(self, image) -> None:
        self.context.mlx.mlx_put_image_to_window(
            self.context.mlx_ptr,
            self._win,
            image.img_ptr,
            0,
            0
        )