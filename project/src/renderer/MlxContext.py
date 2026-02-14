from src.renderer.Viewport import Viewport
from src.renderer.Image import Image
from typing import Type
import sys

class MlxContext:
    # """
    # mlx_binding == mlx.Mlx() -- wrapper instance, binding to MiniLibX backend
    # mlxbinding.mlx == mlxbackend
    # mlxbinding.mlx.mlx_ptr == mlx_ptr (pointer to the running MiniLibX backend)
    # """"
    def __init__(self, mlx_binding: any) -> None:
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
        self.counter = 0

    @property
    def mlxbinding(self) -> any:
        return self._mlxbinding
    
    @property
    def mlx_ptr(self) -> int:
        return self._mlx_ptr

    def get_size(self) -> tuple:
        return self.mlxbinding.get_screen_size(self.mlx_ptr)

    def create_new_viewport(self, w: int, h: int, title: str) -> any:
        viewport = Viewport()
        try:
            viewport.viewport_ptr = self.mlxbinding.mlx_new_window(
                self.mlx_ptr,
                w,
                h,
                title)
            viewport.height = h
            viewport.width = w
            viewport.title = title
            viewport.mlx_ptr = self.mlx_ptr
            if not viewport.viewport_ptr:
                raise Exception(f"Can't create {title} viewport")
        except Exception as e:
            print(f"Error: context at create viewport raised: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"context: viewport {viewport.mlx_ptr} successfully created")
        return viewport

    def create_new_image(self, Img_Class: Image, w: int, h: int) -> Image:
        img = Img_Class()
        try:
            img.img_ptr = self.mlxbinding.mlx_new_image(self.mlx_ptr, w, h)
            img.width = w
            img.height = h
            raw_data, img.bytes_per_pixel, img.stride, img.endian = \
            self.mlxbinding.mlx_get_data_addr(img.img_ptr)
            if not raw_data:
                raise Exception(f"Can't create image data")
        except Exception as e:
            print(f"Error: context at create image raised: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"context: image {img.img_ptr} successfully created")
        img.set_data(raw_data) #casting to memoryview!!!
        return img

    def string_put(self, viewport_ptr: int, start_x: int, start_y: int, font_color: int, string: str) -> None:
        try:
            self.mlxbinding.mlx_string_put(self.mlx_ptr, viewport_ptr, start_x, start_y, font_color, string)
        except Exception as e:
            print(f"Error at context string put: unable to add string to viewport {viewport_ptr}")
        print("Successfully added string to viewport {viewport_ptr}")

    def start_loop(self):
        try:
            print("Starting the mlx loop...")
            self.mlxbinding.mlx_loop(self.mlx_ptr)
        except Exception as e:
            print(f"Error: context at start loop raised: {e}", file=sys.stderr)
            sys.exit(1)         

    def destroy_viewport(self, viewport_ptr: int) -> None:
        try:
            if viewport_ptr:
                print("Destroying viewport")
                self.mlxbinding.mlx_destroy_window(self.mlx_ptr, viewport_ptr)
            else:
                print("provide viewport pointer")
                return
        except Exception as e:
            print(f"Error: context at destroy viewport raised: {e}", file=sys.stderr)
            sys.exit(1)            
    
    def destroy_image(self, image_ptr: int) -> None:
        try:
            if image_ptr:
                print("Destroying image")
                self.mlxbinding.mlx_destroy_image(self.mlx_ptr, image_ptr)
            else:
                print("provide image pointer")
                return
        except Exception as e:
            print(f"Error: context at destroy image raised: {e}", file=sys.stderr)
            sys.exit(1)