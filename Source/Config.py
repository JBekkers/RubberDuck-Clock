import os
import json
import copy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = os.path.join(
    os.getenv("APPDATA"),
    "RubberDuckClock"
)

os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(
    CONFIG_DIR,
    "config.json"
)

DEFAULT_CONFIG = {
    "position": {
        "x": 915,
        "y": 0
    },

    "settings": {
        "hourly_quack": False
    }
}


def load_config():

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        # Add new settings automatically
        for section, values in DEFAULT_CONFIG.items():

            if section not in config:
                config[section] = copy.deepcopy(values)

            else:
                for key, value in values.items():

                    if key not in config[section]:
                        config[section][key] = value

        return config

    except Exception:

        return copy.deepcopy(DEFAULT_CONFIG)


def save_config(config):

    try:
        with open(CONFIG_FILE, "w") as f:

            json.dump(
                config,
                f,
                indent=4
            )

    except Exception:
        pass