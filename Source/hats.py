import json
import os
import random
import time
import logging

from Source.Config.paths import CONFIG_DIR, HATS_DIR


logger = logging.getLogger(__name__)

DROP_INTERVAL_SECONDS = 20 * 60

RARITIES = {
    "Common": {
        "folder": "Common",
        "weight": 60,
        "color": "#949090",
    },
    "Uncommon": {
        "folder": "Uncommon",
        "weight": 25,
        "color": "#06AA00",
    },
    "Rare": {
        "folder": "Rare",
        "weight": 10,
        "color": "#0063D4",
    },
    "Ultra-rare": {
        "folder": "Ultra_Rare",
        "weight": 4,
        "color": "#8C20FF",
    },
    "Legendary": {
        "folder": "Legendary",
        "weight": 1,
        "color": "#EC9427",
    },
}

RARITY_ORDER = [
    "Legendary",
    "Ultra-rare",
    "Rare",
    "Uncommon",
    "Common",
]

INVENTORY_VERSION = 1

HAT_OFFSETS = {
    "afro": (0, 20),
    "rainbow_afro": (0, 20),
    "tophat": (0, 10),
    "diving_goggles": (15, 48),
}

def load_hat_catalog():
    catalog = {}

    for rarity, settings in RARITIES.items():
        folder = os.path.join(
            HATS_DIR,
            settings["folder"]
        )

        if not os.path.isdir(folder):
            logger.warning(
                "Hat rarity folder is missing: %s",
                folder
            )
            continue

        for filename in sorted(os.listdir(folder)):
            if not filename.lower().endswith(".png"):
                continue

            hat_id = os.path.splitext(filename)[0]

            if hat_id in catalog:
                raise ValueError(
                    f"Duplicate hat ID: {hat_id}"
                )

            offset_x, offset_y = HAT_OFFSETS.get(
                hat_id,
                (0, 0)
            )

            catalog[hat_id] = {
                "id": hat_id,
                "name": hat_id.replace("_", " ").title(),
                "rarity": rarity,
                "path": os.path.join(folder, filename),
                "offset_x": offset_x,
                "offset_y": offset_y,
            }

    if not catalog:
        raise RuntimeError(
            f"No hat PNGs found in {HATS_DIR}"
        )

    return catalog


class HatManager:
    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)

        self.inventory_file = os.path.join(
            CONFIG_DIR,
            "hat_inventory.json"
        )

        self.catalog = load_hat_catalog()
        self.owned = []
        self.equipped = None
        self._next_instance_id = 1

        self.next_drop_at = (
            time.time() + DROP_INTERVAL_SECONDS
        )

        self.load_inventory()

    def load_inventory(self):
        if not os.path.exists(self.inventory_file):
            self.save_inventory()
            return

        try:
            with open(
                self.inventory_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Invalid inventory format")

            if data.get("version") not in (1, 2):
                raise ValueError("Unsupported inventory version")

            raw_owned = data.get("owned", [])

            if not isinstance(raw_owned, list):
                raise ValueError("Invalid owned list")

            self.owned = []
            used_instance_ids = set()

            for index, item in enumerate(raw_owned):
                if isinstance(item, str):
                    # Migrate an old inventory entry.
                    hat_id = item
                    instance_id = f"hat_{index + 1}"

                elif isinstance(item, dict):
                    hat_id = item.get("hat_id")
                    instance_id = item.get("instance_id")

                    if not isinstance(instance_id, str):
                        instance_id = f"hat_{index + 1}"

                else:
                    continue

                if hat_id not in self.catalog:
                    continue

                if instance_id in used_instance_ids:
                    instance_id = f"hat_{index + 1}"

                    suffix = 1
                    while instance_id in used_instance_ids:
                        suffix += 1
                        instance_id = f"hat_{index + 1}_{suffix}"

                used_instance_ids.add(instance_id)

                self.owned.append({
                    "instance_id": instance_id,
                    "hat_id": hat_id,
                })

            # Keep equipped selections compatible with both
            # the old and new inventory formats.
            equipped = data.get("equipped")

            if isinstance(equipped, dict):
                equipped = equipped.get("instance_id")

            if isinstance(equipped, str):
                # New format: equipped is an instance ID.
                matching = next(
                    (
                        item for item in self.owned
                        if item["instance_id"] == equipped
                    ),
                    None
                )

                if matching is not None:
                    self.equipped = equipped
                else:
                    # Old format: equipped was a catalog hat ID.
                    matching = next(
                        (
                            item for item in self.owned
                            if item["hat_id"] == equipped
                        ),
                        None
                    )

                    if matching is not None:
                        self.equipped = matching["instance_id"]

            next_drop = data.get("next_drop_at")

            if (
                isinstance(next_drop, (int, float))
                and not isinstance(next_drop, bool)
            ):
                self.next_drop_at = max(
                    time.time(),
                    next_drop
                )

            self._next_instance_id = len(self.owned) + 1

        except (
            OSError,
            ValueError,
            TypeError
        ):
            logger.exception(
                "Could not load hat inventory"
            )

            self.owned = []
            self.equipped = None
            self._next_instance_id = 1

            self.next_drop_at = (
                time.time() + DROP_INTERVAL_SECONDS
            )

        self.save_inventory()

    def save_inventory(self):
        data = {
            "version": 2,
            "owned": self.owned,
            "equipped": self.equipped,
            "next_drop_at": self.next_drop_at,
        }

        temp_file = self.inventory_file + ".tmp"

        try:
            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=2
                )

            os.replace(
                temp_file,
                self.inventory_file
            )

        except OSError:
            logger.exception(
                "Could not save hat inventory"
            )
            raise

    def add_hat(self, hat_id):
        if hat_id not in self.catalog:
            raise ValueError(
                f"Unknown hat ID: {hat_id}"
            )

        instance_id = f"hat_{self._next_instance_id}"
        self._next_instance_id += 1

        self.owned.append({
            "instance_id": instance_id,
            "hat_id": hat_id,
        })

        self.save_inventory()
        return instance_id

    def toggle_hat(self, instance_id):
        if not any(
            item["instance_id"] == instance_id
            for item in self.owned
        ):
            return False

        if self.equipped == instance_id:
            self.equipped = None
        else:
            self.equipped = instance_id

        self.save_inventory()
        return True

    def get_sorted_inventory(self):
        return sorted(
            self.owned,
            key=lambda item: (
                RARITY_ORDER.index(
                    self.catalog[item["hat_id"]]["rarity"]
                ),
                self.catalog[item["hat_id"]]["name"].casefold(),
                item["instance_id"],
            )
        )

    def choose_random_hat(self):
        available_rarities = [
            rarity
            for rarity in RARITY_ORDER
            if any(
                hat["rarity"] == rarity
                for hat in self.catalog.values()
            )
        ]

        if not available_rarities:
            return None

        rarity = random.choices(
            available_rarities,
            weights=[
                RARITIES[rarity]["weight"]
                for rarity in available_rarities
            ],
            k=1
        )[0]

        candidates = [
            hat
            for hat in self.catalog.values()
            if hat["rarity"] == rarity
        ]

        return random.choice(candidates)

    def is_drop_available(self):
        return time.time() >= self.next_drop_at

    def claim_drop(self):
        if not self.is_drop_available():
            return None

        hat = self.choose_random_hat()

        if hat is None:
            return None

        self.add_hat(hat["id"])

        self.next_drop_at = (
            time.time() + DROP_INTERVAL_SECONDS
        )

        self.save_inventory()

        return hat
