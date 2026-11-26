#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to the output directory.

Standard library only. The grader image ships no Pillow and no fonts, so
this program does no drawing at all: it just copies entry.png, which the
repository holds, to /output/entry.png (or $MAKEFUN_OUTPUT_DIR when set).
Deterministic: the same bytes on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
