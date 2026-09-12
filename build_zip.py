from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).parent
OUTPUT = ROOT / "astrbot_plugin_thinking_filter.zip"
FILES = ["__init__.py", "main.py", "metadata.yaml"]

with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
    for name in FILES:
        path = ROOT / name
        archive.write(path, Path("astrbot_plugin_thinking_filter") / name)

print(f"created {OUTPUT}")
