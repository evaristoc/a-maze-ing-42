import sys
from src.renderer.Image import Image
import mlx


class Viewport:
    """Represents a display surface bound to an MLX context."""

    _viewportptr: int
    _height: int
    _width: int
    _title: str

    def __init__(self) -> None:
        """Initialize an empty window with no MLX bindings."""

        self._viewportptr = 0
        self._mlx_ptr = 0
        self._height = 0
        self._width = 0
        self._title = ""

    # getters
    @property
    def viewport_ptr(self) -> int:
        return self._viewportptr

    @viewport_ptr.setter
    def viewport_ptr(self, ptr: int) -> None:
        self._viewportptr = ptr

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, h: int) -> None:
        self._height = h

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, w: int) -> None:
        self._width = w

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, t: str) -> None:
        self._title = t

    @property
    def mlx_ptr(self) -> int:
        return self._mlx_ptr

    @mlx_ptr.setter
    def mlx_ptr(self, mlx_ptr) -> None:
        self._mlx_ptr = mlx_ptr

    def add_img(self, img: Image, x: int = 0, y: int = 0) -> None:
        """Blit an image buffer to the window at given coordinates."""

        if not img:
            raise Exception("pointers to img / context required")
        try:
            mlx.Mlx().mlx_put_image_to_window(
                self._mlx_ptr,
                self._viewportptr,
                img.img_ptr,
                x,
                y
            )
        except Exception as e:
            print(f"Error: viewport at add img raised: {e}", file=sys.stderr)
            sys.exit(1)

    def string_put(
        self,
        start_x: int,
        start_y: int,
        font_color: int,
        string: str
    ) -> None:
        """Render a text string in the window at given position."""

        try:
            mlx.Mlx().mlx_string_put(
                self.mlx_ptr,
                self._viewportptr,
                start_x,
                start_y,
                font_color,
                string
            )
        except Exception as e:
            print(f"Error: viewpot at string put raised: {e}", file=sys.stderr)
            return
        print("viewport: string successfully added")
