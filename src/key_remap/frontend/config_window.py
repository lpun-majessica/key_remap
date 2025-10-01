from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame

from src.key_remap.backend import config_manager
from .utils import (
    get_user_confirmation,
    monospace_font,
    format_key_name,
)


class ConfigRow(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.column_width = 24

        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")
        self.columnconfigure(3, weight=1, uniform="a")


class ConfigHeaderRow(ConfigRow):
    def __init__(self, master):
        super().__init__(master)
        columns = [
            ("From", self.column_width),
            ("To", self.column_width),
            ("Active", self.column_width // 2),
            ("", self.column_width // 2),
        ]
        font = monospace_font(10, "bold")

        for i, (text, width) in enumerate(columns):
            label = ttk.Label(self, text=text, width=width, font=font)
            label.grid(column=i, row=0)


class ConfigDataRow(ConfigRow):
    def __init__(self, master, category: str, config: dict):
        super().__init__(master)
        self.category = category
        self.config = config

        formatted_key_from = format_key_name(self.config["from"])
        formatted_key_to = format_key_name(self.config["to"])

        self.key_from_text = ttk.StringVar()
        self.key_to_text = ttk.StringVar()
        self.checkbox_boolean = BooleanVar()

        self.key_from_text.set(formatted_key_from)
        self.key_to_text.set(formatted_key_to)
        self.checkbox_boolean.set(
            self.config["active"] if "active" in self.config else True
        )

        self.key_from = ttk.Label(
            self, textvariable=self.key_from_text, width=self.column_width
        )
        self.key_to = ttk.Label(
            self, textvariable=self.key_to_text, width=self.column_width
        )
        self.checkbox = ttk.Checkbutton(
            self,
            variable=self.checkbox_boolean,
            command=self.handle_toggle_checkbox,
        )
        self.delete_button = ttk.Button(
            self, text="Delete", bootstyle="secondary", command=self.delete
        )

    def populate(self):
        ttk.Separator(self, orient="horizontal").grid(
            column=0, columnspan=4, row=0, sticky="news", padx=5, pady=5
        )
        self.key_from.grid(column=0, row=1, padx=5)
        self.key_to.grid(column=1, row=1, padx=5)
        self.checkbox.grid(column=2, row=1, sticky="news", padx=23)
        self.delete_button.grid(column=3, row=1)

    def delete(self):
        key_from = format_key_name(self.config["from"])
        key_to = format_key_name(self.config["to"])

        is_confirmed = get_user_confirmation(
            title="Delete",
            icon="warning",
            message=f'Delete config "{key_from} - {key_to}"?',
        )
        if is_confirmed:
            config_manager.delete_config(self.category, self.config["from"])
            self.destroy()

    def handle_toggle_checkbox(self):
        config_manager.edit_config(self.category, self.config["from"])
        self.bell()

    def bind_function(self, event, func):
        self.bind(event, func)
        self.key_from.bind(event, func)
        self.key_to.bind(event, func)

    def change_config(self, key_to: str):
        self.config["to"] = key_to
        formatted_key_to = format_key_name(key_to)
        self.key_to_text.set(formatted_key_to)


class ConfigList(ScrolledFrame):
    def __init__(self, master, category: str, height: int = 250):
        super().__init__(master, padding="15 10", height=height)
        self.category = category
        self.rows = dict()

        self.header = ConfigHeaderRow(self)
        self.header.pack(expand=False, fill="x")

    def populate(self, configs: dict):
        for config in configs.values():
            self.add_new_row(config)

    def add_new_row(self, config: dict):
        row = ConfigDataRow(self, self.category, config)
        row.populate()
        row.pack(expand=False, fill="x")

        self.rows[config["from"]] = row

    def delete_all_rows(self):
        for row in self.winfo_children():
            if row != self.header:
                row.destroy()


class ConfigWindow(ttk.Frame):
    def __init__(self, master, height: int = 200, width: int = 680):
        super().__init__(master, height=height)
        self.tabs = dict()
        self.window = ttk.Notebook(self, height=height, width=width)
        self.window.pack(expand=True, fill="y", anchor="center", padx=10)

    def load_config(self, all_configs: dict[str, dict]):
        for category, configs in all_configs.items():
            list_title = category.title()
            config_list = ConfigList(self, category)
            config_list.populate(configs)

            self.window.add(config_list.container, text=list_title)
            self.tabs[category] = config_list

    def add_config(self, category: str, config: dict):
        self.tabs[category].add_new_row(config)

    def reset_all_configs(self):
        is_confirmed = get_user_confirmation(
            title="Reset all", icon="warning", message=f"Reset ALL configs?"
        )

        if is_confirmed:
            config_manager.reset_all_config()

            for tab in self.tabs.values():
                tab.delete_all_rows()
