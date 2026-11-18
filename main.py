"""news-image-20261118: write the held front-page image to the output path.

The repository holds the finished 1024x1024 PNG (entry.png) — a newspaper
front page summing up the world's news of Wednesday 18 November 2026 — and
this program copies it to /output/entry.png. Standard library only, no
network, and byte-identical output on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Deterministic check: the copy must be byte-complete, or fail loudly.
    if os.path.getsize(src) != os.path.getsize(dst):
        raise RuntimeError("entry.png copy is incomplete")


if __name__ == "__main__":
    main()
