class Image():
    _width: int
    _height: int

    def __init__(self) -> None:
        self._img = None
        self._data = None
        self._int_view = None
        self._bpp = 0
        self._sl = 0
        self._endian = 0
        self._width = 0
        self._height = 0

    #getters
    @property
    def img_ptr(self):
        return self._img

    @property
    def data(self):
        return self._data

    @property
    def bytes_per_pixel(self):
        return self._bpp

    @property
    def stride(self):
        return self._sl

    @property
    def endian(self):
        return self._endian

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    #setters
    @img_ptr.setter
    def img_ptr(self, img_ptr: any) -> None:
        self._img = img_ptr

    @data.setter
    def data(self, data: any) -> None:
        self._data = data

    @bytes_per_pixel.setter
    def bytes_per_pixel(self, bpp: int) -> None:
        self._bpp = bpp

    @stride.setter
    def stride(self, sl: int) -> None:
        self._sl = sl

    @endian.setter
    def endian(self, endian: int) -> None:
        self._endian = endian

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    # def put_pixel(self, x: int, y: int, color: int) -> None:
    #     if x < 0 or y < 0 or x >= self.width or y >= self.height:
    #         return
    #     bytes_per_pixel = self._bpp // 8
    #     offset = y * self._sl + x * bytes_per_pixel
    #     if offset + bytes_per_pixel - 1 >= len(self._data):
    #         return
    #     self._write_color(offset, color)

    # #TODO: BE CAREFUL WITH THIS ONE NOW...
    # def _write_color(self, offset: int, color: int) -> None:
    #     self._data[offset + 0] = color & 0xFF
    #     self._data[offset + 1] = (color >> 8) & 0xFF
    #     self._data[offset + 2] = (color >> 16) & 0xFF
    #     self._data[offset + 3] = (color >> 24) & 0xFF

    # after casting!!!
    def put_pixel(self, x: int, y: int, color: int) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        pixel_offset = (y * (self.stride // 4)) + x
        try:
            self._int_view[pixel_offset] = color
        except Exception as e:
            print(f"Error writing pixel: {e}")

    #same as above but simpler
    def clear(self, color: int = 0x00000000):
        print(f"image: clearing image {self.img_ptr}")
        pixel_count = self.width * self.height
        self._data[:] = (color.to_bytes(4, byteorder="little")) * pixel_count

    # Casting into memoryview allows python to be closer to low level by writing directly to raw memory address!!! (Gemini)
    def set_data(self, raw_data: list) -> None:
        # We wrap the pointer in a memoryview
        self._data = memoryview(raw_data).cast('B') # Raw bytes
        # This is the secret: a view that treats the buffer as 32-bit integers
        self._int_view = self._data.cast('I')


class ImageBuffer(Image):
    """writable, frame-owned"""
    pass

class ImageAsset(Image):
    """read-only, loaded"""
    pass