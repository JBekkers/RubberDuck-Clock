import json
import os
import random
import time
import logging

from Source.Config.paths import CONFIG_DIR, HATS_DIR


logger = logging.getLogger(__name__)

DROP_INTERVAL_SECONDS = 15 * 60

RARITIES = {
    "Common": {
        "folder": "Common",
        "weight": 60,
        "color": "#808080",
    },
    "Uncommon": {
        "folder": "Uncommon",
        "weight": 25,
        "color": "#90D69A",
    },
    "Rare": {
        "folder": "Rare",
        "weight": 10,
        "color": "#438DE0",
    },
    "Ultra-rare": {
        "folder": "Ultra_Rare",
        "weight": 4,
        "color": "#A46BE0",
    },
    "Legendary": {
        "folder": "Legendary",
        "weight": 1,
        "color": "#E89A39",
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
    "diving_goggles": (15, 50),
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

            if data.get("version") != INVENTORY_VERSION:
                raise ValueError("Unsupported inventory version")

            owned = data.get("owned", [])

            if not isinstance(owned, list):
                raise ValueError("Invalid owned list")

            self.owned = [
                hat_id
                for hat_id in owned
                if isinstance(hat_id, str)
                and hat_id in self.catalog
            ]

            equipped = data.get("equipped")

            if (
                isinstance(equipped, str)
                and equipped in self.owned
            ):
                self.equipped = equipped

            next_drop = data.get("next_drop_at")

            if (
                isinstance(next_drop, (int, float))
                and not isinstance(next_drop, bool)
            ):
                self.next_drop_at = max(
                    time.time(),
                    next_drop
                )

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

            self.next_drop_at = (
                time.time() + DROP_INTERVAL_SECONDS
            )

        self.save_inventory()

    def save_inventory(self):
        data = {
            "version": INVENTORY_VERSION,
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

        self.owned.append(hat_id)
        self.save_inventory()

    def toggle_hat(self, hat_id):
        if hat_id not in self.owned:
            return False

        if self.equipped == hat_id:
            self.equipped = None
        else:
            self.equipped = hat_id

        self.save_inventory()
        return True

    def get_sorted_inventory(self):
        return sorted(
            enumerate(self.owned),
            key=lambda item: (
                RARITY_ORDER.index(
                    self.catalog[item[1]]["rarity"]
                ),
                item[0]
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

        self.owned.append(hat["id"])

        self.next_drop_at = (
            time.time() + DROP_INTERVAL_SECONDS
        )

        self.save_inventory()

        return hat