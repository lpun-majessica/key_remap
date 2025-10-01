from src.key_remap.backend import config_manager, undo_all
from src.key_remap.frontend import UI


def on_close():
    undo_all()
    ui.quit_window()


def on_open():
    ui.show_window()


def on_reset():
    ui.show_window()
    ui.after(0, ui.config_window.reset_all_configs)


systray_menu = [("Open", on_open), ("Reset all", on_reset), ("Quit", on_close)]
ui = UI(systray_menu=systray_menu)


def run():
    ui.config_window.load_config(config_manager.config)
    ui.protocol("WM_DELETE_WINDOW", ui.hide_window)

    config_manager.start()
    ui.start()
