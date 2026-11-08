"""
Branding of the DAW — product name and logo in one place.

The name matches the Catalogue Manager (Music_catalogue_manager_v.2/config.py)
and can be overridden with the same environment variable SBS_BRAND_NAME.
"""
from __future__ import annotations

import os
import sys

BRAND_NAME: str = os.environ.get("SBS_BRAND_NAME", "Beat Collage")
APP_NAME: str = "DAW"                       # shown next to the brand name
WINDOW_TITLE: str = f"{BRAND_NAME}  ·  {APP_NAME}"


def asset_path(*parts: str) -> str:
    """Absolute path inside daw_light_version/assets (works in PyInstaller builds too)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, "assets", *parts)


LOGO_MARK: str = asset_path("brand", "logo-mark.svg")
