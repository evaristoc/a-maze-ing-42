import sys
from src.renderer.Image import Image

class Viewport():
    _viewportptr: int
    _height : int
    _width : int
    _context : int
    _main_buffer : any
    title : str
    def __init__(self) -> None:
        self._viewportptr = 0
        self._mlx_ptr = 0
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
    def mlx_ptr(self) -> None:
        return self._mlx_ptr

    @property
    def imgbuffer(self) -> None:
        return self._main_buffer

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

    @context.setter
    def context(self, context: any) -> None:
        self._context = context

    @context.setter
    def imgbuffer(self, img: Image) -> None:
        self._main_buffer = img

    @mlx_ptr.setter
    def mlx_ptr(self, mlx_ptr) -> None:
        self._mlx_ptr = mlx_ptr

    ## for buffering a single, modifiable image
    def add_img(self, image) -> None:
        #TODO
        if not image:
            raise Exception("Image can not be null")
        if not self._context:
            raise Exception("There is no context associated to this window/viewport")
        backend = self._context
        mlx_pointer = self._mlx_ptr
        self._main_buffer = backend.mlx_put_image_to_window(
            mlx_pointer,
            self._viewportptr,
            image.img_ptr,
            0,
            0
        )
        if not self._main_buffer:
            raise Exception("Can't add image to viewport")