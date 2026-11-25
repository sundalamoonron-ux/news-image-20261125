#!/usr/bin/env python3
"""news-image-20261125 entry: write the day's front page to /output/entry.png.

The image shipped beside this file sums up Wednesday 25 November 2026 in
one page: the Cartagena supermarket siege plus five more stories from
around the world. Standard library only, no network, deterministic —
the same bytes on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
source = HERE / "entry.png"
if not source.is_file():
    raise SystemExit("entry.png is missing beside main.py")
target = OUT / "entry.png"
shutil.copyfile(source, target)
if target.stat().st_size != source.stat().st_size:
    raise SystemExit("entry.png did not copy completely")
with target.open("rb") as fh:
    if fh.read(8) != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
