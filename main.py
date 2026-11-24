#!/usr/bin/env python3
"""Entry for make.fun news-image-20261124 (Python 3.13, stdlib only).

Copies the front-page image beside this file to the output directory
named by MAKEFUN_OUTPUT_DIR (default /output) as entry.png.
No network, no clock, no randomness: the same input always
produces the same output bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
# The competition gate refuses images over 1 MiB, so check the copy
# we just wrote and fail loudly instead of submitting a bad file.
MAX_BYTES = 1048576

os.makedirs(OUT, exist_ok=True)
dest = os.path.join(OUT, "entry.png")
shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
size = os.path.getsize(dest)
if size == 0 or size > MAX_BYTES:
    raise SystemExit("entry.png is %d bytes, outside the 1 MiB gate" % size)
