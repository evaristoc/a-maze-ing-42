from typing import Any


class Image:
    """Represents a writable base image with pixel access."""

    _img: int
    _data: memoryview
    _int_view: memoryview
    _bpp: int
    _sl: int
    _endian: int
    _width: int
    _height: int

    def __init__(self) -> None:
        """Initialize an empty image with no allocated buffer."""

        memview = memoryview(bytearray())
        self._img = 0
        self._data = memview
        self._int_view = memview
        self._bpp = 0
        self._sl = 0
        self._endian = 0
        self._width = 0
        self._height = 0

    # getters and setters
    @property
    def img_ptr(self) -> Optional[int]:
        return self._img

    @img_ptr.setter
    def img_ptr(self, imgptr: int) -> None:
        self._img = imgptr

    @property
    def data(self) -> Optional[memoryview]:
        return self._data

    @data.setter
    def data(self, data: Optional[memoryview]) -> None:
        self._data = data

    @property
    def bytes_per_pixel(self) -> int:
        return self._bpp

    @bytes_per_pixel.setter
    def bytes_per_pixel(self, bpp: int) -> None:
        self._bpp = bpp

    @property
    def stride(self) -> int:
        return self._sl

    @stride.setter
    def stride(self, sl: int) -> None:
        self._sl = sl

    @property
    def endian(self) -> int:
        return self._endian

    @endian.setter
    def endian(self, endian: int) -> None:
        self._endian = endian

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, w: int) -> None:
        self._width = w

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, h: int) -> None:
        self._height = h

    # after casting!!!
    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Write a pixel color at given coordinates if within bounds."""

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        pixel_offset = (y * (self.stride // 4)) + x
        try:
            self._int_view[pixel_offset] = color
        except Exception as e:
            print(f"Error writing pixel: {e}")

    def clear(self, color: int = 0x00000000):
        """Fill the entire image buffer with a single color."""

        print(f"image: clearing image {self.img_ptr}")
        if self._data is not None:
            pixel_count = self.width * self.height
            self._data[:] = (color.to_bytes(4, byteorder="little")) * pixel_count

    # Casting into memoryview allows python to be closer to
    # low level by writing directly to raw memory address!!! (Gemini)
    def set_data(self, raw_data: Any) -> None:
        """Bind raw image memory and create typed buffer views."""

        # We wrap the pointer in a memoryview:
        # casting pointer to raw bytes
        self._data = memoryview(raw_data).cast('B')

        # This is the secret: a view that treats the buffer as 32-bit integers
        self._int_view = self._data.cast('I')


class ImageBuffer(Image):
    """Concrete writable image buffer owned by a render frame."""
    pass
