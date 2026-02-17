import mlx
import sys

def loop_handler(params: list) -> None:
    context, viewport, img, renderer = params
    if not renderer.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(img)
        return
    renderer.animations["globals"]["frame_count"] += 1
    if renderer.animations["globals"]["frame_count"] % 1 != 0:
        viewport.add_img(img)
        return 0
    if renderer.renderer_queue[0] == "background":
        renderer.draw(img, renderer.animations["elements"]["background"]["target"],  {"background":renderer.animations["elements"]["background"]["color"]})
        renderer.draw(img, [renderer.animations["elements"]["fourtytwo"]["target"]], {"fourtytwo":renderer.animations["elements"]["fourtytwo"]["in_color"]})
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(renderer.animations["elements"]["walls"]["target"], None)
        if current is not None:
            renderer.draw(img, [[current]], {"walls":renderer.animations["elements"]["walls"]["color"]})
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(img, [renderer.animations["elements"]["exit"]["target"]], {"exit": renderer.animations["elements"]["exit"]["in_color"]})
        renderer.draw(img, [renderer.animations["elements"]["entry"]["target"]], {"entrance": renderer.animations["elements"]["entry"]["in_color"]})
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "path":
        current = next(renderer.animations["elements"]["path"]["target"], None)
        if current is not None:
            renderer.draw(img, [[current]], {"path": renderer.animations["elements"]["path"]["in_color"]})
        else:
            renderer.renderer_queue.pop(0)
    viewport.add_img(img)
    return 0

def exit_loop(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
        sys.exit(1)

def vis_path(params: list) -> int:
    # params: [viewport, img, renderer, state]
    _, viewport, img, renderer, state = params
    print("Path handling...")
    if not renderer.animations["elements"]["path"]["on"]:
        for c, d in state:
            renderer.draw(img, [[(c, d)]], {"path": renderer.animations["elements"]["path"]["in_color"]})
            renderer.animations["elements"]["path"]["on"] = True
    else:
        for c, d in state:
            print(c, d)
            renderer.draw(img, [[(c, d)]], {"path": renderer.animations["elements"]["background"]["color"]})
            renderer.animations["elements"]["path"]["on"] = False
    viewport.add_img(img)         
    return

def key_handler_factory(keycode: int, params: list) -> int:
    update = params.pop()
    if keycode == 65307: # ESC key
        exit_loop(params[0].mlx_ptr)
        return 0
    if keycode == 112: # 'p' key
        vis_path(params)
    if keycode == 114: # 'r' key
        update(params)
        
    return 0