import copy
import json
import os

import time

from Source.Config.paths import CONFIG_DIR
from Source.Config.error_handler import logger

APP_START_TIME = time.monotonic()

STATS_FILE = os.path.join(
    CONFIG_DIR,
    "stats.json"
)


DEFAULT_STATS = {
    "session_count": 0,
    "total_uptime": 0,
    "rare_animations_seen": 0,
    "rare_animations_discovered": [],
    "rare_animation_counts": {}
}


def load_stats():
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

        if not isinstance(stats, dict):
            raise ValueError(
                "Statistics root must be a JSON object."
            )

        for key, default_value in DEFAULT_STATS.items():
            value = stats.get(key)

            if key not in stats:
                stats[key] = copy.deepcopy(default_value)
                continue

            if key in (
                "session_count",
                "total_uptime",
                "rare_animations_seen",
            ):
                if (
                    not isinstance(value, (int, float))
                    or isinstance(value, bool)
                    or value < 0
                ):
                    stats[key] = copy.deepcopy(default_value)

            elif key == "rare_animations_discovered":
                if not isinstance(value, list):
                    stats[key] = copy.deepcopy(default_value)

            elif key == "rare_animation_counts":
                if (
                    not isinstance(value, dict)
                    or any(
                        not isinstance(v, int)
                        or isinstance(v, bool)
                        or v < 0
                        for v in value.values()
                    )
                ):
                    stats[key] = copy.deepcopy(default_value)

        return stats

    except (OSError, ValueError, TypeError):
        logger.exception("Failed to load statistics.")
        return copy.deepcopy(DEFAULT_STATS)


def save_stats(stats):
    temp_file = STATS_FILE + ".tmp"

    try:
        with open(temp_file, "w") as f:
            json.dump(
                stats,
                f,
                indent=4
            )

            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file, STATS_FILE)
        return True

    except Exception:
        logger.exception(
            "Failed to save statistics."
        )

        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except OSError:
            pass

        return False


def start_session(stats):
    stats["session_count"] = (
        stats.get("session_count", 0) + 1
    )

    save_stats(stats)

def get_session_uptime():

    return time.monotonic() - APP_START_TIME

def add_uptime(stats, seconds):
    stats["total_uptime"] = (
        stats.get("total_uptime", 0)
        + seconds
    )

    save_stats(stats)


def record_rare_animation(stats, name):
    stats["rare_animations_seen"] = (
        stats.get("rare_animations_seen", 0) + 1
    )

    discovered = stats.setdefault(
        "rare_animations_discovered",
        []
    )

    if name not in discovered:
        discovered.append(name)

    counts = stats.setdefault(
        "rare_animation_counts",
        {}
    )

    counts[name] = counts.get(name, 0) + 1

    save_stats(stats)