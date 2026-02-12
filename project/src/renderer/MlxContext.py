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

    @property
    def mlxbinding(self) -> any:
        return self._mlxbinding

    # @property
    # def mlxbackend(self) -> any:
    #     return self._mlxbinding.mlx
    
    @property
    def mlx_ptr(self) -> any:
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
            viewport.p_binding = self._mlxbinding #to add to viewport the ability to eventually add images
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
            img.data, img.bytes_per_pixel, img.stride, img.endian = \
            self.mlxbinding.mlx_get_data_addr(img.img_ptr)
            if not img.data:
                raise Exception(f"Can't create image data")
        except Exception as e:
            print(f"Error: context at create image raised: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"context: image {img.img_ptr} successfully created")
        return img
    
    def start_loop(self):
        try:
            print("Starting the mlx loop...")
            self.mlxbinding.mlx_loop(self.mlx_ptr)
        except Exception as e:
            print(f"Error: context at start loop raised: {e}", file=sys.stderr)
            sys.exit(1)         

    def destroy_window(self, viewport_ptr: any):
        try:
            print("Destroying window")
            self.mlxbinding.mlx_destroy_window(self.mlx_ptr, viewport_ptr)
        except Exception as e:
            print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
            sys.exit(1)            
    def destroy_image():
        #TODO
        pass