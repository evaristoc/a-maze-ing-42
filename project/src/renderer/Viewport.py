import sys
from src.renderer.Image import Image

class Viewport():
    _viewportptr: int
    _height : int
    _width : int
    title : str
    def __init__(self) -> None:
        self._viewportptr = 0
        self._mlx_ptr = 0
        self.height = 0
        self.width = 0
        self.title = ""

    @property
    def viewport_ptr(self) -> None:
        return self._viewportptr

    @property
    def height(self) -> None:
        return self._height

    @property
    def width(self) -> None:
        return self._width

    @property
    def title(self) -> None:
        return self._title
    
    @property
    def mlx_ptr(self) -> None:
        return self._mlx_ptr

    @viewport_ptr.setter
    def viewport_ptr(self, ptr: int) -> None:
        self._viewportptr = ptr

    @height.setter
    def height(self, h: int) -> None:
        self._height = h

    @width.setter
    def width(self, w: int) -> None:
        self._width = w

    @title.setter
    def title(self, t: str) -> None:
        self._title = t

    @mlx_ptr.setter
    def mlx_ptr(self, mlx_ptr) -> None:
        self._mlx_ptr = mlx_ptr

    ## for buffering a single, modifiable image
    def add_img(self, img_ptr: int, x: int = 0, y: int = 0) -> None:
        if not img_ptr or not mxl_pointer:
            raise Exception("pointers to img / context required")
        try:
            mlx.Mlx().mlx.mlx_put_image_to_window(
                self._mlx_ptr,
                self._viewportptr,
                img_ptr,
                x,
                y
            )
        except Exception as e:
            print(f"Error: viewporrt at add img raised: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"viewport: image {img_ptr} successfully added")