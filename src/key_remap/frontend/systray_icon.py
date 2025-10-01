from pystray import Icon, Menu, MenuItem
from PIL import Image

from .utils import ICON_FILE_PATH


class SysTrayIcon(Icon):
    def __init__(self, menu, *args, **kwargs):
        icon_image = self.get_icon_image()
        menu_items = Menu(*[MenuItem(*item) for item in menu])
        super().__init__(icon=icon_image, menu=menu_items, *args, **kwargs)

    @staticmethod
    def get_icon_image():
        return Image.open(ICON_FILE_PATH)
