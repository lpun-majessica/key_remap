import ttkbootstrap as ttk

from src.key_remap.utils.input import detect_key


class DetectorBase(ttk.Toplevel):
    def __init__(self):
        super().__init__(padx=10, pady=10)

        text = "Press any key to continue..."
        text_frame = ttk.Frame(self)
        ttk.Label(text_frame, text=text).pack(anchor="center")
        text_frame.pack(fill="both", anchor="center", padx=20, pady="40 45")

        self.buttons = ttk.Frame(self)

    def start(self, on_start):
        self.place_window_center()
        self.focus()
        self.after(100, on_start)
        self.mainloop()


class KeyDetector(DetectorBase):
    def __init__(self, set_key):
        super().__init__()
        self.title("Key Detector")
        self.set_key = set_key

        self.start(self.detect_key)

    def detect_key(self):
        key = detect_key()
        if key is not None:
            self.set_key(key)
        self.destroy()


class DetectorWindow(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
