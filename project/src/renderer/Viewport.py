import sys
from src.renderer.Image import Image

class Viewport():
    _viewportptr: int
    _height : int
    _width : int
    _binding : int
    _main_buffer : any
    title : str
    def __init__(self) -> None:
        self._viewportptr = 0
        self._mlx_ptr = 0
        self.height = 0
        self.width = 0
        self.title = ""
        self._binding = None
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
    def p_binding(self) -> None:
        return self._binding
    
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

    @p_binding.setter
    def p_binding(self, binding: any) -> None:
        self._binding = binding

    @imgbuffer.setter
    def imgbuffer(self, img: Image) -> None:
        self._main_buffer = img

    @mlx_ptr.setter
    def mlx_ptr(self, mlx_ptr) -> None:
        self._mlx_ptr = mlx_ptr

    ## for buffering a single, modifiable image
    def add_img(self, image: Image) -> None:
        if not image:
            raise Exception("Added image can not be null")
        if not self._binding:
            raise Exception("There is no context associated to this window/viewport")
        binding = self._binding
        mlx_pointer = self._mlx_ptr
        try:
            binding.mlx_put_image_to_window(
                mlx_pointer,
                self._viewportptr,
                image.img_ptr,
                0,
                0
            )
            self._main_buffer = image
            if not self._main_buffer:
                raise Exception("Can't add image to viewport")
        except Exception as e:
            print(f"Error: viewporrt at add img raised: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"viewport: image {image.img_ptr} successfully added")