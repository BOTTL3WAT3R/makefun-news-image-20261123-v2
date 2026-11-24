#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261123 (v2).

Copies the committed poster (entry.png, next to this file) to
/output/entry.png. Standard library only; no network; deterministic -
every run writes exactly the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def validate_image(path: str) -> bool:
    """Self-check: the poster must be a whole PNG within the bounty gate
    (at most 1 MiB, at most 1024x1024 pixels)."""
    import struct

    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > 1048576:
        return False
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    width, height = struct.unpack(">II", data[16:24])
    return width <= 1024 and height <= 1024


def main() -> int:
    if not os.path.isfile(SRC):
        print(f"source image missing: {SRC}", file=sys.stderr)
        return 1
    if not validate_image(SRC):
        print(f"source image fails gate self-check: {SRC}", file=sys.stderr)
        return 1
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
