import sys
from typing import cast

import mlx

from src.renderer.AppResources import AppResources

def mouse_event(button, x, y, params) -> int:
    print(f"Got mouse : {button} at {x}x{y}")
    print(params.image.width, params.buttons["path"].width)
    print(params.image.height, params.buttons["path"].height)
    middle_green_btn_h = params.image.height + int(params.buttons["path"].height / 2)
    middle_green_btn_w = int(params.image.width / 2) + int(params.buttons["path"].width / 2)
    if button == 1:
        if (x >= middle_green_btn_w - 35 and x <= middle_green_btn_w - 20) and (y <= middle_green_btn_h + 15 and y >= middle_green_btn_h - 5):
            print(1111)
            return 1
        return 0

def loop_handler(params: list) -> None:
    viewport, image, renderer, buttons = params
    anims = renderer.animations
    glob_anims = anims.get("globals")
    elem_anims = anims.get("elements")
    if not renderer.renderer_queue:
        # maze
        viewport.add_img(image)
        # path button
        viewport.add_img(buttons["path"],
        int((image.width - buttons["path"].width ) / 2)
        if image.width > buttons["path"].width else 0,
        image.height + 3)
        # reload button
        viewport.add_img(buttons["reload"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + buttons["path"].height + 2* 3)
        # walls button
        viewport.add_img(buttons["walls"],
        int((image.width - buttons["walls"].width ) / 2)
        if image.width > buttons["walls"].width else 0,
        image.height + 2 * buttons["reload"].height + 3 * 3)
        # esc
        viewport.add_img(buttons["esc"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + 3 * buttons["reload"].height + 4 * 3)
        return
    glob_anims["frame_count"] += 1
    if glob_anims.get("frame_count") % 1 != 0:
        # maze
        viewport.add_img(image)
        # path button
        viewport.add_img(buttons["path"],
        int((image.width - buttons["path"].width ) / 2)
        if image.width > buttons["path"].width else 0,
        image.height + 3)
        # reload button
        viewport.add_img(buttons["reload"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + buttons["path"].height + 2* 3)
        # walls button
        viewport.add_img(buttons["walls"],
        int((image.width - buttons["walls"].width ) / 2)
        if image.width > buttons["walls"].width else 0,
        image.height + 2 * buttons["reload"].height + 3 * 3)
        # esc
        viewport.add_img(buttons["esc"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + 3 * buttons["reload"].height + 4 * 3)

        return
    if renderer.renderer_queue[0] == "background":
        renderer.draw(
            image,
            elem_anims.get("background").get("target"),
            {"background": elem_anims.get("background").get("color")}
        )
        renderer.draw(
            image,
            [elem_anims.get("fourtytwo").get("target")],
            {"fourtytwo": elem_anims.get("fourtytwo").get("in_color")}
        )
        print("background ready")
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "walls":
        current = next(elem_anims.get("walls").get("target"), None)
        if current is not None:
            renderer.draw(
                image,
                [[current]],
                {"walls": elem_anims.get("walls").get("color")}
            )
        else:
            renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "doors":
        renderer.draw(
            image,
            [elem_anims.get("exit").get("target")],
            {"exit": elem_anims.get("exit").get("in_color")}
        )
        renderer.draw(
            image,
            [elem_anims.get("entry").get("target")],
            {"entrance": elem_anims.get("entry").get("in_color")}
        )
        renderer.renderer_queue.pop(0)
    elif renderer.renderer_queue[0] == "path":
        current = next(elem_anims.get("path").get("target"), None)
        if current is not None:
            renderer.draw(
                image,
                [[current]],
                {"path": elem_anims.get("path").get("in_color")}
            )
        else:
            renderer.renderer_queue.pop(0)
        
        # Adding images
        # maze
        viewport.add_img(image)
        # path button
        viewport.add_img(buttons["path"],
        int((image.width - buttons["path"].width ) / 2)
        if image.width > buttons["path"].width else 0,
        image.height + 3)
        # reload button
        viewport.add_img(buttons["reload"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + buttons["path"].height + 2* 3)
        # walls button
        viewport.add_img(buttons["walls"],
        int((image.width - buttons["walls"].width ) / 2)
        if image.width > buttons["walls"].width else 0,
        image.height + 2 * buttons["reload"].height + 3 * 3)
        # esc
        viewport.add_img(buttons["esc"],
        int((image.width - buttons["reload"].width ) / 2)
        if image.width > buttons["reload"].width else 0,
        image.height + 3 * buttons["reload"].height + 4 * 3)


def exit_loop_handler(mlx_ptr: int) -> None:
    try:
        print("Exiting the mlx loop...")
        mlx.Mlx().mlx_loop_exit(mlx_ptr)
    except Exception as e:
        print(
            f"Error: context at destroy window raised: {e}",
            file=sys.stderr
        )
        sys.exit(1)


def vis_path_handler(params: list) -> int:
    viewport, image, renderer = params
    animation = cast(dict, renderer.animations.get("elements"))
    elem_anim = cast(dict, animation.get("path"))
    sol_path = cast(list, cast(dict, animation.get("path")).get("target_all"))
    print("Path handling...")
    if not elem_anim.get("on"):
        for c, d in sol_path:
            renderer.draw(
                image,
                [[(c, d)]],
                {"path": elem_anim.get("in_color")}
            )
            elem_anim["on"] = True
    else:
        background = cast(dict, animation.get("background"))
        for c, d in sol_path:
            renderer.draw(
                image,
                [[(c, d)]],
                {"path": background.get("color")}
            )
            elem_anim["on"] = False
    viewport.add_img(image)
    return 0


def wall_color_handler(params: list) -> int:
    viewport, image, renderer = params
    animation = cast(dict, renderer.animations.get("elements"))
    elem_anim = cast(dict, animation.get("walls"))
    walls = cast(list, cast(dict, animation.get("walls")).get("target_all"))
    print("Walls handling...")
    if elem_anim.get("on"):
        for c in walls:
            renderer.draw(image, [[c]], {"walls": 0xFFFFFFFF})
            elem_anim["on"] = False
    else:
        for c in walls:
            renderer.draw(
                image, [[c]], {"walls": elem_anim.get("color")}
            )
            elem_anim["on"] = True
    viewport.add_img(image)
    return 0


def key_handler_controller(
    keycode: int, params: AppResources
) -> int:
    if keycode == 65307:  # ESC key
        exit_loop_handler(params.context.mlx_ptr)
        return 0
    if keycode == 112:  # 'p' key
        visparams = [params.viewport, params.image, params.renderer]
        vis_path_handler(visparams)
    if keycode == 119:  # 'w' key
        wallparams = [params.viewport, params.image, params.renderer]
        wall_color_handler(wallparams)
    if keycode == 114:  # 'r' key
        update = cast(object, params.update_func)
        if callable(update):
            update(params)
    return 0
