# from dataclasses import dataclass
from typing import Optional, Callable
from src.renderer.MlxContext import MlxContext
from src.renderer.Image import Image
from src.renderer.Viewport import Viewport
from src.renderer.RendererEngine import Renderer


class AppResources:
    context: MlxContext
    viewport: Optional[Viewport] = None
    image: Optional[Image] = None
    renderer: Optional[Renderer] = None
    update_func: Optional[Callable] = None
    config_file: str = ""
    ui_viewport: Optional[Viewport] = None
