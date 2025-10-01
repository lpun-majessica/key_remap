from enum import Enum
from ttkbootstrap.dialogs import Messagebox

ICON_FILE_PATH = "./img/icon.ico"


class Themes(Enum):
    Light = "minty"
    Dark = "darkly"


class Categories(Enum):
    KeyMap = "keymap"


def monospace_font(size: int | str = "", weight="") -> str:
    return f"Consolas {size} {weight}".strip()


def get_user_confirmation(*args, **kwargs) -> bool:
    return Messagebox.yesno(*args, **kwargs)


def format_key_name(key: str | None) -> str | None:
    if not key:
        return None
    return key.title()
