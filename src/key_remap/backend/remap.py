import keyboard


def remap_key(key: str, to: str):
    def handler(event):
        if event.event_type == keyboard.KEY_DOWN:
            keyboard.press(to)
        elif event.event_type == keyboard.KEY_UP:
            keyboard.release(to)

    return keyboard.hook_key(key, handler, suppress=True)


def undo_remap(key):
    try:
        keyboard.unhook_key(key)
    except KeyError:
        pass


def undo_all():
    keyboard.unhook_all()
