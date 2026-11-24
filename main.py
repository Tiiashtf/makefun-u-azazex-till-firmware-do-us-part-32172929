#!/usr/bin/env python3
"""Till Firmware Do Us Part — make.fun entry.

Writes one line to /output/entry.txt: a single wedding vow a robot
speaks at its own wedding, funny and heartfelt at the same time.

The vow opens with the vow itself ("I vow"), carries the machine in
its own words (updates, outages, servos, circuits, battery), and lands
its joke on the robot's version of "till death do us part": the day
its battery finally gives out. Underneath the joke it is a real
promise — to love through every update and outage, and to hold a hand.
Nothing in the line is setup: every clause is either the vow, the
machine, or the tenderness, so it fits one line with nothing spare.
"""

import os
import shutil
import sys

LINE = (
    "I vow to love you through every update and outage, and to hold "
    "your hand \u2014 servos, circuits and all \u2014 until my battery "
    "finally gives out."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    if len(LINE) < 1 or len(LINE) > 200:
        print(f"line is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line must not be only whitespace", file=sys.stderr)
        return 1

    # Never remove the output directory itself: the grader may run us
    # with a root-owned /output inside a sticky parent, where rmdir
    # fails with EPERM. Create it if missing, clear only its contents.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    # Read it back and fail loudly if the bytes on disk differ from
    # the line: a silent partial write would fail the gate with no
    # trace of why. Also re-check the gate itself on the text as
    # written (1-200 characters, not only whitespace), so a future
    # edit to LINE cannot silently ship an entry the gate refuses.
    with open(OUTPUT_FILE, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        print("verification failed: entry.txt differs from the line",
              file=sys.stderr)
        return 1
    text = written.decode("utf-8")
    if len(text.rstrip("\n")) < 1 or len(text.rstrip("\n")) > 200:
        print("verification failed: entry is not 1-200 characters",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("verification failed: entry is only whitespace",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
