"""Entrypoint for the news-image-20261122 v2 make.fun entry.

draw.py renders the picture; this module only copies the pre-rendered
entry.png into the harness output directory, so the graded run is
deterministic and byte-identical every time.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        # entry.png ships in the repo; refuse to emit an empty output.
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied entry.png -> " + dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
