import json
import os
from importlib import resources


def load_config(config_path: str | None = None) -> dict:
    default_config = _load_default_config()
    chosen_path = config_path or os.getenv("BREAKPOINT_CONFIG")
    if not chosen_path:
        return default_config

    with open(chosen_path, "r", encoding="utf-8") as f:
        custom = json.load(f)
    return _deep_merge(default_config, custom)


def _load_default_config() -> dict:
    package = "breakpoint.config"
    resource = resources.files(package).joinpath("default_policies.json")
    with resource.open("r", encoding="utf-8") as f:
        return json.load(f)


def _deep_merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
