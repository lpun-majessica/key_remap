from tkinter import font
import ttkbootstrap as ttk

from .config_window import ConfigWindow
from .detector import DetectorWindow
from .systray_icon import SysTrayIcon
from .utils import (
    monospace_font,
    Themes,
    Categories,
    ICON_FILE_PATH,
)

DEFAULT_CATEGORY = Categories.KeyMap.value


class UI(ttk.Window):
    def __init__(self, systray_menu):
        self.NAME = "Key Remap"
        minsize = (800, 600)
        default_theme = Themes.Dark.value

        super().__init__(
            title=self.NAME,
            themename=default_theme,
            minsize=minsize,
            iconphoto=None,
        )

        self.iconbitmap(ICON_FILE_PATH, default=ICON_FILE_PATH)
        self.systray_icon = None
        self.systray_menu = systray_menu

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Consolas")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self, padding="20 15")

        self.top_section = ttk.Frame(self.mainframe)
        app_name_font = monospace_font("16", "bold")
        self.app_name = ttk.Label(
            master=self.top_section, text=self.NAME, font=app_name_font
        )

        def change_theme():
            new_theme = self.theme.get()
            self.style.theme_use(new_theme)

        self.theme = ttk.StringVar(value=default_theme)
        self.theme_options = ttk.Frame(self.top_section)
        for theme in Themes:
            radio_button = ttk.Radiobutton(
                self.theme_options,
                text=theme.name,
                variable=self.theme,
                value=theme.value,
                command=change_theme,
            )
            radio_button.pack(side="left", padx=10, expand=True)

        self.separator1 = ttk.Separator(self.mainframe, orient="horizontal")

        self.detector_window = DetectorWindow(
            self.mainframe, DEFAULT_CATEGORY, self.update_config_list
        )

        self.separator2 = ttk.Separator(self.mainframe, orient="horizontal")

        self.config_window = ConfigWindow(self.mainframe)

        self.buttons = ttk.Frame(self.mainframe)
        ttk.Button(
            self.buttons,
            text="Reset all",
            bootstyle="secondary",
            command=self.config_window.reset_all_configs,
        ).pack(side="left", anchor="se", padx="5 20", pady="15 0")

    def show_window(self):
        self.systray_icon.stop()
        self.after(0, self.deiconify)

    def hide_window(self):
        self.withdraw()
        self.systray_icon = self.create_systray_icon()
        self.systray_icon.run()

    def quit_window(self):
        self.systray_icon.stop()
        self.destroy()

    def create_systray_icon(self):
        return SysTrayIcon(name="icon", title=self.NAME, menu=self.systray_menu)

    def start(self):
        self.mainframe.grid(column=0, row=0, sticky="news")

        self.top_section.pack(fill="x", padx=10, pady=10)
        self.app_name.pack(side="left")
        self.theme_options.pack(side="right")

        self.separator1.pack(fill="x", padx=10, pady="2 15")
        self.detector_window.pack(anchor="center")

        self.separator2.pack(fill="x", padx=10, pady=10)
        self.config_window.pack(expand=True, fill="both")
        self.buttons.pack(anchor="se", pady="5 15")

        self.place_window_center()
        self.after(1, self.hide_window)
        self.mainloop()

    def update_config_list(self, category, config, overwrite=False):
        if overwrite:
            key_from, key_to = config["from"], config["to"]
            self.config_window.tabs[category].rows[key_from].change_config(key_to)
        else:
            self.config_window.add_config(category, config)
