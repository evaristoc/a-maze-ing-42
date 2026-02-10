import sys
from .MlxContext import MlxContext
from .Image import Image

class ViewPort:
    _viewportptr: int
    _height : int
    _width : int
    _context : int
    _main_buffer : any
    title : str
    def __init__(self) -> None:
        self._viewportptr = 0
        self.height = 0
        self.width = 0
        self.title = ""
        self._context = None
        self._main_buffer = None

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
    def context(self) -> None:
        return self._context

    @property
    def imgbuffer(self) -> None:
        return self._main_buffer

    @viewport_ptr.setter
    def viewport_ptr(self, ptr: int) -> None:
        self._viewportptr = ptr

    @property
    def height(self, h: int) -> None:
        self._height = h

    @property
    def width(self, w: int) -> None:
        self._width = w

    @property
    def title(self, t: str) -> None:
        self._title = t

    @property
    def context(self, context: Mlx) -> None:
        self._context = context

    @property
    def imgbuffer(self, img: Image) -> None:
        self._main_buffer = img

    ## for buffering a single, modifiable image
    def add_img(self, image) -> None:
        #TODO
        if not image:
            raise Exception("Image can not be null")
        if not self._context:
            raise Exception("There is no context associated to this window/viewport")
        backend = self._context.mlxbackend
        mlx_pointer = self._context.mlx_ptr
        self._main_buffer = self.backend.mlx_put_image_to_window(
            self.mlx_pointer,
            self._viewportptr,
            image.img_ptr,
            0,
            0
        )
        if not self._main_buffer:
            raise Exception("Can't add image to viewport")