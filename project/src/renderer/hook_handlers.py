import mlx
from typing import Type

def loop_handler(params: list) -> None:
    context, viewport, renderer = params
    if not renderer.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(context.img_asset)
        return
    renderer.animations["globals"]["frame_count"] += 1
    if renderer.animations["globals"]["frame_count"] % 1 != 0:
        viewport.add_img(context.img_asset)
        return 0
    if renderer.renderer_queue[0] == "background":
        renderer.draw(context.img_asset, renderer.animations["elements"]["background"]["target"],  {"background":renderer.animations["elements"]["background"]["color"]})
        renderer.draw(context.img_asset, [renderer.animations["elements"]["fourtytwo"]["target"]], {"fourtytwo":renderer.animations["elements"]["fourtytwo"]["in_color"]})
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(renderer.animations["elements"]["walls"]["target"], None)
        if current is not None:
            renderer.draw(context.img_asset, [[current]], {"walls":renderer.animations["elements"]["walls"]["color"]})
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(context.img_asset, [renderer.animations["elements"]["exit"]["target"]], {"exit": renderer.animations["elements"]["exit"]["in_color"]})
        renderer.draw(context.img_asset, [renderer.animations["elements"]["entry"]["target"]], {"entrance": renderer.animations["elements"]["entry"]["in_color"]})
        renderer.renderer_queue.pop(0)
    viewport.add_img(context.img_asset)
    return 0

def close_viewport_handler(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
        sys.exit(1) 


