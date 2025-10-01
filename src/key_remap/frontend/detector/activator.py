import ttkbootstrap as ttk

from .detector import KeyDetector
from src.key_remap.frontend.utils import monospace_font, format_key_name, Categories


class DetectorActivator(ttk.LabelFrame):
    def __init__(self, master, category, text: str, width: int = 15):
        super().__init__(master, text=f" {text} ", padding=10, width=width)
        font = monospace_font(14, "bold")

        self.category = category
        self.key = None
        self.label_text = ttk.StringVar()
        self.label = ttk.Label(
            self,
            textvariable=self.label_text,
            font=font,
            width=width,
            anchor="center",
            wraplength=400,
            justify="center",
        )
        self.key_detector = None

        self.buttons = ttk.Frame(self)
        ttk.Button(self.buttons, text="Register", command=self.open_detector).pack(
            side="right", padx=5
        )
        ttk.Button(
            self.buttons, text="Undo", bootstyle="secondary", command=self.undo
        ).pack(side="right", padx=5)

    def display(self):
        self.label.pack(fill="both", padx=10, pady="30 20", anchor="center")
        self.buttons.pack(pady=5, anchor="center")

    def set_key(self, key):
        self.key = key
        formatted_key = format_key_name(self.key)
        self.label_text.set(formatted_key)

    def undo(self):
        self.key = None
        self.label_text.set("")

    def open_detector(self):
        current_category = self.category
        if current_category == Categories.KeyMap.value:
            KeyDetector(set_key=self.set_key)
