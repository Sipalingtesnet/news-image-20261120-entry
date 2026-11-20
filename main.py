#!/usr/bin/env python3
"""Copy the pre-generated entry.png to the output directory.

Stdlib only: shutil + hashlib. Deterministic, no network.
"""
import hashlib
import os
import shutil
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(REPO_DIR, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.exists(SRC):
        print("entry.png not found in repo", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    digest = sha256(OUT)
    print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())