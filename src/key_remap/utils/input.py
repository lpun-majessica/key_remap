import keyboard


def detect_key():
    event = keyboard.read_event(suppress=False)
    if event.event_type == keyboard.KEY_DOWN:
        return event.name
    return None
