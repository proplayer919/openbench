import json
import os
from typing import Any, Dict

SETTINGS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../settings.json")
)
DEFAULT_SETTINGS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "default.json")
)


def load_settings() -> Dict[str, Any]:
    # Load default settings
    with open(DEFAULT_SETTINGS_PATH, "r") as f:
        default_settings = json.load(f)

    # Try to load top-level settings.json
    try:
        if not os.path.exists(SETTINGS_PATH) or os.path.getsize(SETTINGS_PATH) == 0:
            raise FileNotFoundError("settings.json missing or empty")
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        if not isinstance(settings, dict):
            raise ValueError("settings.json malformed")
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        settings = {}

    # Fill missing keys from default
    updated = False
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
            updated = True

    # If settings was empty or updated, write back to settings.json
    if updated or not settings:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4)

    return settings
