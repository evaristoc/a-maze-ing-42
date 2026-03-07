import sys
from typing import Optional
import mlx

from src.renderer.Image import Image, RasterImage
from src.renderer.Viewport import Viewport


class MlxContext:
    """Manage MLX context, windows, images, and main loop lifecycle."""

    def __init__(self, mlx_binding: mlx.Mlx) -> None:
        """Initialize MLX backend and store root mlx pointer."""
        try:
            self._mlxbinding = mlx_binding
            self._mlx_ptr = self._mlxbinding.mlx_init()
            if not self._mlx_ptr:
                raise RuntimeError("mlx_init() failed to return a pointer")
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)
        self.counter = 0

    @property
    def mlxbinding(self) -> mlx.Mlx:
        return self._mlxbinding

    @property
    def mlx_ptr(self) -> int:
        return int(self._mlx_ptr)

    def get_size(self) -> tuple[int, ...]:
        """Get size of whole context surface."""
        return tuple(self.mlxbinding.get_screen_size(self.mlx_ptr))

    def create_new_viewport(
        self, w: int, h: int, title: str
    ) -> Viewport:
        """Create and register a new MLX display surface."""
        viewport = Viewport()
        try:
            viewport.viewport_ptr = self.mlxbinding.mlx_new_window(
                self.mlx_ptr, w, h, title
            )
            viewport.height = h
            viewport.width = w
            viewport.title = title
            viewport.mlx_ptr = self.mlx_ptr
            if not viewport.viewport_ptr:
                raise Exception(f"Can't create {title} viewport")
        except Exception as e:
            print(
                f"Error: context at create viewport raised: {e}",
                file=sys.stderr
            )
            sys.exit(1)
        print(f"context: viewport {viewport.mlx_ptr} successfully created")
        return viewport

    def create_new_image(
        self, Img_Class: type[Image], w: int, h: int
    ) -> Image:
        """Create MLX image and attach memoryview-backed buffer."""
        try:
            img.img_ptr = self.mlxbinding.mlx_new_image(
                self.mlx_ptr, w, h
            )
            if not img.img_ptr:
                raise Exception("Could not create image")
            img = Img_Class()
            img.width = w
            img.height = h
            raw_data, img.bytes_per_pixel, img.stride, img.endian = \
                self.mlxbinding.mlx_get_data_addr(img.img_ptr)
            if not raw_data:
                raise Exception("Can't create image data")
        except Exception as e:
            print(
                f"Error: context at create image raised: {e}",
                file=sys.stderr
            )
            sys.exit(1)
        img.set_data(raw_data)
        print(f"context: image {img.img_ptr} successfully created")
        return img

    def load_image(
        self,
        asset_path: str
    ) -> Optional[Image]:
        """Add external raster images into a desired position."""        
        img = RasterImage()
        try:
            result = self.mlxbinding.mlx_png_file_to_image(
               self.mlx_ptr,
               asset_path                
            )
            if not result:
               raise Exception("Can't create png")
            img_ptr, w, h = result
            img.img_ptr = img_ptr
            img.width = w
            img.height = h
            raw_data, img.bytes_per_pixel, img.stride, img.endian = \
                self.mlxbinding.mlx_get_data_addr(img.img_ptr)
            if not raw_data:
                raise Exception("Can't create raster - png - data")
        except Exception as e:
            print(
                f"Error: context at add raster raised: {e}",
                file=sys.stderr
            )
            return
        img.set_data(raw_data)
        print(f"context: image {img.img_ptr} successfully created")
        return img

    def start_loop(self) -> None:
        """Start MLX event loop and block until exit."""
        try:
            print("Starting the mlx loop...")
            self.mlxbinding.mlx_loop(self.mlx_ptr)
        except Exception as e:
            print(
                f"Error: context at start loop raised: {e}",
                file=sys.stderr
            )
            sys.exit(1)

    def destroy_viewport(self, viewport_ptr: int) -> None:
        """Destroy MLX window associated with given pointer."""
        try:
            if viewport_ptr:
                print("Destroying viewport")
                self.mlxbinding.mlx_destroy_window(
                    self.mlx_ptr, viewport_ptr
                )
            else:
                print("provide viewport pointer")
                return
        except Exception as e:
            print(
                f"Error: context at destroy viewport raised: {e}",
                file=sys.stderr
            )
            sys.exit(1)

    def destroy_image(self, image_ptr: int) -> None:
        """Destroy MLX image associated with given pointer."""
        try:
            if image_ptr:
                print("Destroying image")
                self.mlxbinding.mlx_destroy_image(
                    self.mlx_ptr, image_ptr
                )
            else:
                print("provide image pointer")
                return
        except Exception as e:
            print(
                f"Error: context at destroy image raised: {e}",
                file=sys.stderr
            )
            sys.exit(1)
