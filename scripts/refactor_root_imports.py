#!/usr/bin/env python3
"""Rewrite legacy root-module imports after moving code into typhoon_vn.

The command is a dry run by default. It only rewrites imports; moving files is a
separate, deliberate step.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


MODULE_MAP: dict[str, str] = {
    "data_loader": "typhoon_vn.datasets.legacy_dataset",
    "model": "typhoon_vn.models.legacy_lstm",
    "train": "typhoon_vn.training.legacy_train",
    "predict": "typhoon_vn.inference.legacy_predict",
    "draw_map": "typhoon_vn.visualization.track_map",
    "share_func": "typhoon_vn.features.legacy_preprocessing",
}


@dataclass(frozen=True)
class Replacement:
    start: int
    end: int
    text: str


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert imports of legacy root modules to package-relative imports."
    )
    parser.add_argument(
        "--package-root",
        type=Path,
        default=Path("src/typhoon_vn"),
        help="Package directory to scan (default: src/typhoon_vn).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--write", action="store_true", help="Update files in place."
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Print only a summary and exit 1 when rewrites are required.",
    )
    return parser


def _character_column(line: str, utf8_column: int) -> int:
    """Translate an AST UTF-8 byte offset into a Python string offset."""
    return len(line.encode("utf-8")[:utf8_column].decode("utf-8"))


def _absolute_offset(
    lines: Sequence[str], line_starts: Sequence[int], lineno: int, column: int
) -> int:
    return line_starts[lineno - 1] + _character_column(lines[lineno - 1], column)


def _current_package(file: Path, package_root: Path) -> list[str]:
    relative = file.relative_to(package_root)
    return [package_root.name, *relative.parent.parts]


def _relative_module(file: Path, package_root: Path, target_module: str) -> str:
    current = _current_package(file, package_root)
    target = target_module.split(".")
    if not target or target[0] != package_root.name:
        raise ValueError(
            f"target {target_module!r} is outside package {package_root.name!r}"
        )
    common = 0
    for current_part, target_part in zip(current, target):
        if current_part != target_part:
            break
        common += 1
    dots = "." * (len(current) - common + 1)
    suffix = ".".join(target[common:])
    return dots + suffix


def _node_span(
    node: ast.AST, lines: Sequence[str], line_starts: Sequence[int]
) -> tuple[int, int]:
    if not hasattr(node, "end_lineno") or node.end_lineno is None:
        raise ValueError("Python 3.11+ AST positions are required")
    start = _absolute_offset(lines, line_starts, node.lineno, node.col_offset)
    end = _absolute_offset(
        lines, line_starts, node.end_lineno, node.end_col_offset
    )
    return start, end


def rewrite_source(
    source: str, file: Path, package_root: Path
) -> tuple[str, list[str]]:
    """Return rewritten source and diagnostics for unsupported old imports."""
    tree = ast.parse(source, filename=str(file))
    lines = source.splitlines(keepends=True)
    if not lines:
        return source, []
    line_starts: list[int] = []
    offset = 0
    for line in lines:
        line_starts.append(offset)
        offset += len(line)
    replacements: list[Replacement] = []
    diagnostics: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level != 0 or node.module not in MODULE_MAP:
                continue
            start, end = _node_span(node, lines, line_starts)
            statement = source[start:end]
            marker = f"from {node.module}"
            marker_at = statement.find(marker)
            if marker_at < 0:
                diagnostics.append(
                    f"{file}:{node.lineno}: unsupported formatting for {marker!r}"
                )
                continue
            module_start = start + marker_at + len("from ")
            module_end = module_start + len(node.module)
            replacements.append(
                Replacement(
                    module_start,
                    module_end,
                    _relative_module(file, package_root, MODULE_MAP[node.module]),
                )
            )
            continue
        if isinstance(node, ast.Import):
            old_aliases = [alias for alias in node.names if alias.name in MODULE_MAP]
            if not old_aliases:
                continue
            if len(node.names) != 1:
                diagnostics.append(
                    f"{file}:{node.lineno}: split a mixed/multiple import before migration"
                )
                continue
            alias = old_aliases[0]
            target = MODULE_MAP[alias.name]
            parent, leaf = target.rsplit(".", 1)
            imported_name = alias.asname or alias.name
            relative_parent = _relative_module(file, package_root, parent)
            start, end = _node_span(node, lines, line_starts)
            replacements.append(
                Replacement(
                    start,
                    end,
                    f"from {relative_parent} import {leaf} as {imported_name}",
                )
            )
    rewritten = source
    for replacement in sorted(replacements, key=lambda item: item.start, reverse=True):
        rewritten = (
            rewritten[: replacement.start]
            + replacement.text
            + rewritten[replacement.end :]
        )
    return rewritten, diagnostics


def _read_python(path: Path) -> str:
    with tokenize.open(path) as handle:
        return handle.read()


def run(package_root: Path, *, write: bool, check: bool) -> int:
    package_root = package_root.resolve()
    if not package_root.is_dir():
        print(f"error: package root does not exist: {package_root}", file=sys.stderr)
        return 2
    if not (package_root / "__init__.py").is_file():
        print(f"error: not a regular Python package: {package_root}", file=sys.stderr)
        return 2
    changed = 0
    diagnostics: list[str] = []
    for path in sorted(package_root.rglob("*.py")):
        try:
            before = _read_python(path)
            after, file_diagnostics = rewrite_source(before, path, package_root)
        except (SyntaxError, UnicodeError, ValueError) as exc:
            diagnostics.append(f"{path}: {exc}")
            continue
        diagnostics.extend(file_diagnostics)
        if before == after:
            continue
        changed += 1
        display = path.relative_to(package_root.parent)
        if write:
            path.write_text(after, encoding="utf-8", newline="")
            print(f"rewrote {display}")
        elif not check:
            print(
                "".join(
                    difflib.unified_diff(
                        before.splitlines(keepends=True),
                        after.splitlines(keepends=True),
                        fromfile=str(display),
                        tofile=str(display),
                    )
                ),
                end="",
            )
    for diagnostic in diagnostics:
        print(f"error: {diagnostic}", file=sys.stderr)
    action = "rewritten" if write else "requiring rewrite"
    print(f"{changed} file(s) {action}")
    if diagnostics:
        return 2
    if check and changed:
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    return run(args.package_root, write=args.write, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
