import os
import json
import copy

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
    "total_uptime": 0,
    
    "position": {
        "x": 915,
        "y": 0
    },

    "settings": {
    "hourly_quack": False,
    "always_on_top": True,
    "disable_animation": False,
    "disable_sound": False,
    "disable_particles": False,

    "auto_timezone": True,
    "timezone": "Europe/Amsterdam",
    "clock_24_hour": True,
    }
}


def load_config():

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        # Add missing top-level sections/settings
        for section, default_value in DEFAULT_CONFIG.items():

            if section not in config:
                config[section] = copy.deepcopy(default_value)

            elif isinstance(default_value, dict):
                for key, value in default_value.items():

                    if key not in config[section]:
                        config[section][key] = copy.deepcopy(value)

        return config

    except Exception as e:

        print(f"Failed to load config: {e}")

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