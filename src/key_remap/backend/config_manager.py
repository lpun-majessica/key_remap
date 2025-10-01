import yaml

from .remap import remap_key, undo_remap, undo_all

CONFIG_FILE = "./config.yml"
DEFAULT_CONFIG = {"keymap": {}}


class ConfigManager:
    def __init__(self):
        self.config: dict = self.read_config()

    def start(self):
        for category, configs in self.config.items():
            for config in configs.values():
                if not config["active"]:
                    continue
                try:
                    self.load_config(category, config)
                except ValueError as e:
                    print(e)

    @staticmethod
    def read_config(path=CONFIG_FILE):
        try:
            file = open(path, "a+")
            config = yaml.safe_load(file)
            return config if config else DEFAULT_CONFIG
        except yaml.YAMLError as e:
            print(e)

    @staticmethod
    def load_config(category, config):
        key_from = config["from"]
        key_to = config["to"]

        if category == "keymap":
            return remap_key(key_from, key_to)
        else:
            raise ValueError("Unknown category")

    def save_config(self, path=CONFIG_FILE):
        file = open(path, "w")
        return yaml.dump(self.config, file)

    def add_config(self, category, config):
        key = config["from"]
        self.config[category][key] = config
        self.save_config()

        if config["active"]:
            self.load_config(category, config)

    def reset_all_config(self):
        self.config = {category: dict() for category in self.config}
        undo_all()
        self.save_config()

    def delete_config(self, category, key):
        del self.config[category][key]
        self.save_config()
        undo_remap(key)

    def overwrite_config(self, category, config):
        key = config["from"]
        self.config[category][key] = config

        self.delete_config(category, key)
        self.add_config(category, config)
        self.save_config()

    def edit_config(self, category, key):
        config = self.config[category][key]
        is_active = config["active"]

        self.config[category][key]["active"] = not is_active
        self.save_config()

        if is_active:
            undo_remap(key)
        else:
            self.load_config(category, config)

    def check_existing_mappings(self, key: str):
        return self.config["keymap"].get(key, None)
