import copy
import json
import os

from Source.Config.paths import CONFIG_DIR


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
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)

        for key, default_value in DEFAULT_STATS.items():
            if key not in stats:
                stats[key] = copy.deepcopy(default_value)

        return stats

    except Exception as e:
        print(f"Failed to load stats: {e}")
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

        os.replace(temp_file,STATS_FILE)

    except Exception as e:
        print(f"Failed to save stats: {e}")

        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception:
            pass


def start_session(stats):
    stats["session_count"] = (
        stats.get("session_count", 0) + 1
    )

    save_stats(stats)


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