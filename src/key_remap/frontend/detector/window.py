import ttkbootstrap as ttk

from src.key_remap.backend import config_manager

from .activator import DetectorActivator
from src.key_remap.frontend.utils import format_key_name


class DetectorWindow(ttk.Frame):
    def __init__(self, master, category, add_config, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.detector_from = DetectorActivator(self, category, text="From:")
        self.detector_to = DetectorActivator(self, category, text="To:")

        self.add_button = ttk.Button(
            self, text="Add", state="disabled", command=add_config
        )

        self.detector_from.label_text.trace("w", self.is_valid_to_save)
        self.detector_to.label_text.trace("w", self.is_valid_to_save)

        self.display()

    def display(self):
        self.detector_from.display()
        self.detector_to.display()

        self.detector_from.pack(side="left", padx="30 5", pady=5, anchor="center")
        self.detector_to.pack(side="left", padx=5, pady=5, anchor="center")
        self.add_button.pack(side="left", padx="10 5", pady=5, anchor="center")

    def is_valid_to_save(self, *args):
        key_from = self.detector_from.key
        key_to = self.detector_to.key

        if key_from and key_to and key_from != key_to:
            existing_config = config_manager.check_existing_mappings(key_from)

            if not existing_config or (
                existing_config and existing_config["to"] != key_to
            ):
                self.add_button.configure(state="normal")
            else:
                self.add_button.configure(state="disabled")
        else:
            self.add_button.configure(state="disabled")

    def get_keys(self):
        return self.detector_from.key, self.detector_to.key

    def set_keys(self, key_from, key_to):
        formatted_key_from = format_key_name(key_from)
        formatted_key_to = format_key_name(key_to)

        self.detector_from.key = key_from
        self.detector_to.key = key_to

        self.detector_from.label_text.set(formatted_key_from)
        self.detector_to.label_text.set(formatted_key_to)
