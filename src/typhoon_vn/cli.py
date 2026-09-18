"""Small command-line entry points reserved for the delivery phases."""

from __future__ import annotations

import argparse


def main() -> None:
    """Dispatch scaffolding commands without implying later phases are complete."""

    parser = argparse.ArgumentParser(prog="typhoon-vn")
    parser.add_argument("command", choices=("clean-data", "train"))
    args = parser.parse_args()

    commands = {
        "clean-data": "Data cleaning is scheduled for Phase 2; no raw data was modified.",
        "train": "Model training is scheduled for Phases 3–4; no training was started.",
    }
    print(commands[args.command])


if __name__ == "__main__":
    main()
