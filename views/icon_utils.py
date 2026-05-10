import base64
import os
from functools import lru_cache
from html import escape


_ICON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))


def icon_path(filename):
    return os.path.join(_ICON_DIR, filename)


@lru_cache(maxsize=None)
def _svg_data_uri(filename):
    with open(icon_path(filename), "rb") as icon_file:
        encoded = base64.b64encode(icon_file.read()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def svg_icon_html(filename, size=20, alt="", style=""):
    alt_text = escape(alt, quote=True)
    return (
        f'<img src="{_svg_data_uri(filename)}" alt="{alt_text}" '
        f'style="width:{size}px;height:{size}px;display:inline-block;vertical-align:middle;{style}" />'
    )