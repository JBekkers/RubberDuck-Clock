from Source.Config.config import save_config


def toggle_hourly_quack(settings, config):

    settings["hourly_quack"] = not settings["hourly_quack"]

    save_config(config)