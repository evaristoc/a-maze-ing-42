import mlx

def loop_animations(params: list) -> None:
    context, viewport, renderer, target = params
    if not context.renderer_queue:
        # Optimization: We still put the image to keep the window alive/responsive
        viewport.add_img(context.img_asset)
        return
    context.counter += 1
    if context.counter % 500 != 0:
        viewport.add_img(context.img_asset)
        return 0
    if context.renderer_queue[0] == "background":
        renderer.draw(context.img_asset, target, {"background": 0xFF2200FF})
        renderer.draw(context.img_asset, target, {"fourtytwo": 0xFFFFFFFF})
        context.renderer_queue.pop(0)
    elif context.renderer_queue[0] == "walls":
        renderer.draw(context.img_asset, target, {"walls": 0xFF00AAAA})
        context.renderer_queue.pop(0)
    elif context.renderer_queue[0] == "doors":
        renderer.draw(context.img_asset, target, {"entrance": 0xFF00FF00, "exit": 0xFFFF00FF})
        context.renderer_queue.pop(0)
    viewport.add_img(context.img_asset)
    return 0 


