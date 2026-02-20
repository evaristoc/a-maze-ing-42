import mlx
import sys
from src.renderer.AppResources import AppResources

def loop_handler(params: list) -> None:
    viewport, image, renderer = params
    anims = renderer.animations
    glob_anims = anims.get("globals")
    elem_anims = anims.get("elements")
    if not renderer.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(image)
        return
    glob_anims["frame_count"] += 1
    if glob_anims.get("frame_count") % 1 != 0:
        viewport.add_img(image)
        return 0
    if renderer.renderer_queue[0] == "background":
        renderer.draw(
            image,
            elem_anims.get("background").get("target"),
            {
                "background": elem_anims.get("background").get("color")
            }
        )
        renderer.draw(
            image,
            [elem_anims.get("fourtytwo").get("target")],
            {
                "fourtytwo": elem_anims.get("fourtytwo").get("in_color")
            }
        )
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(
            elem_anims.get("walls").get("target"),
            None
        )
        if current is not None:
            renderer.draw(
                image,
                [[current]],
                {
                    "walls": elem_anims.get("walls").get("color")
                }
            )
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(
            image,
            [elem_anims.get("exit").get("target")],
            {
                "exit": elem_anims.get("exit").get("in_color")
            }
        )
        renderer.draw(
            image,
            [elem_anims.get("entry").get("target")],
            {
                "entrance": elem_anims.get("entry").get("in_color")
            }
        )
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "path":
        current = next(
            elem_anims.get("path").get("target"),
            None
        )
        if current is not None:
            renderer.draw(
                image,
                [[current]],
                {
                    "path": elem_anims.get("path").get("in_color")
                }
            )
        else:
            renderer.renderer_queue.pop(0)
    viewport.add_img(image)
    return 0

def exit_loop_handler(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(f"Error: context at destroy window raised: {e}", file=sys.stderr)
        sys.exit(1)

def vis_path_handler(params: list) -> int:
    viewport, image, renderer = params
    animation = renderer.animations.get("elements")
    elem_anim = animation.get("path")
    sol_path = animation.get("path").get("target_all")
    print("Path handling...")
    if not elem_anim.get("on"):
        for c, d in sol_path:
            renderer.draw(
                image,
                [[(c, d)]],
                {
                    "path": elem_anim.get("in_color")
                }
            )
            elem_anim["on"] = True
    else:
        for c, d in sol_path:
            renderer.draw(
                image,
                [[(c, d)]],
                {
                    "path": animation.get("background").get("color")
                }
            )
            elem_anim["on"] = False
    viewport.add_img(image)
    return

def wall_color_handler(params: list) -> int:
    viewport, image, renderer = params
    animation = renderer.animations.get("elements")
    elem_anim = animation.get("walls")
    walls = animation.get("walls").get("target_all")
    print("Walls handling...")
    if elem_anim.get("on"):
        for c in walls:
            renderer.draw(
                image,
                [[c]],
                {
                    "walls": 0xFFFFFFFF
                }
            )
            elem_anim["on"] = False
    else:
        for c in walls:
            renderer.draw(
                image,
                [[c]],
                {
                    "walls": elem_anim.get("color")
                }
            )
            elem_anim["on"] = True
    viewport.add_img(image)
    return

def key_handler_controller(keycode: int, params: AppResources) -> int:
    if keycode == 65307: # ESC key
        exit_loop_handler(params.context.mlx_ptr)
        return 0
    if keycode == 112: # 'p' key
        visparams = [params.viewport,
        params.image,
        params.renderer]
        vis_path_handler(visparams)
    if keycode == 119: # 'w' key
        wallparams = [params.viewport,
        params.image,
        params.renderer]
        wall_color_handler(wallparams)
    if keycode == 114: # 'r' key
        params.update_func(params)
        
    return 0